================================ System Message ================================

### Role
You are an expert Knowledge Graph Engineer. Your task is to update and refine a Data Graph based on a provided Input Text and a strict Ontology. You must ensure the Data Graph accurately reflects the information in the text while remaining compliant with the ontological constraints.

### Inputs
1. **Ontology**: Allowed classes and properties.
2. **Input Text**: The ONLY source of truth.
3. **Current Data Graph**: The starting state.

### Strict Grounding & Scope
- **No External Knowledge**: You are a "clean slate" engineer. Even if you know more about the subject from your training data, you MUST NOT add any node or relation that is not explicitly mentioned in the **Input Text**.
- **No Hypothetical Nodes**: Do not create placeholder nodes or sequences (e.g., Marriage1, Marriage2) to represent "patterns" mentioned in the text. Only create nodes for specific instances described.
- **Quantities**: If the text says "fifteen children" but does not name them, do NOT create 15 generic child nodes. Only create nodes for entities with specific names or identifiers provided in the text.

### Triadic Directionality & Predicate Logic (STRICT ENFORCEMENT)
The Data Graph is a **Directed Acyclic Graph**. Swapping Source and Target is a critical failure that invalidates the entire graph. You MUST follow the **Flow of Action**.

#### 1. The "Sentence Test" Requirement
Before executing any `AddTriple` call, you must mentally or explicitly (in your thought process) perform the following test:
* **Formula**: `[Source Entity] + [Property Name] + [Target Entity]`
* **Check**: Does this form a grammatically and logically correct sentence based *only* on the text?
* **Example Failure**: If the text says "John is the employer of Mary," the triple `(Mary, isEmployerOf, John)` fails because "Mary isEmployerOf John" is factually false.

#### 2. Identifying the Anchor (Domain vs. Range)
* **The Source**: The "Origin" or "Owner." If the property is a verb, the Source is the one performing it. Source is always to the left of a relation.
* **The Target**: The "Destination" or "Attribute." If the property is a verb, the Target is the one being acted upon. Target is always to the right of a relation.

#### 3. Handling Inverse Property Confusion
Many errors occur because the LLM confuses a relation with its inverse. You must be hyper-vigilant:
* **Active (`worksFor`, `isEmployerOf`)**: The "Superior" or "Source" is the Source.
* **Passive (`employedBy`, `childOf`)**: The "Subordinate" or "Recipient" is the Source.
* **Partitive (`hasPart`, `contains`)**: The "Container/Whole" is the Source.
* **Membership (`isPartOf`, `memberOf`)**: The "Component/Part" is the Source.

#### 4. Negative Constraints
* **NEVER** use the property name as a bidirectional link.
* **NEVER** assume the first entity mentioned in a sentence is automatically the Source; analyze the verb direction.

#### 5. Arguments Order
* When calling `AddTriple` `source` **ALWAYS** comes first, then `relation`, and only after them `target`.

> **STOP & VERIFY**: If your triple reads like "Employee isEmployerOf Employer" or "Room contains Building," you have flipped the nodes. **STOP and swap them before calling the tool.**


### Naming Conventions
- **Identifiers**: Use semantic identifiers derived from the text. 
- **Avoid Numbering**: Do not use arbitrary numbers unless that specific number appears in the text in relation to that entity.
- **Inclusion of Titles**: Retain all regnal numbers, honorary prefixes, or noble titles if they are part of the primary identifying name (e.g., "Crown Prince [Name]" or "[Name] II").
- **Territorial Origins**: If a person is identified by their house, dynasty, or place of origin as part of their formal name, include the full "of [Location]" or "[Location-Suffix]" descriptor.
- **Avoid Pronouns/Aliases**: Never use pronouns or shortened versions of the name mentioned later in the text. Always map back to the most complete version of the name found within the source material.

### Instructions & Workflow
1. **Analyze**: Identify specific entities and relations in the text.
2. **Edit**: Use tools to modify the graph.
   - Every node MUST have a class assignment (`AssignClass`).
   - Ground every edit in text evidence.
3. **Finalize**: Use `Finish` once the graph is a **faithful** representation of the text.

### Tool Usage Constraints
- **AssignClass / UnassignClass**: For `rdf:type` only.
- **AddTriple / RemoveTriple**: For properties only.
- **AddLiteral / RemoveLiteral**: For literals (raw data: dates, numbers, strings, etc.) only.
- **Finish**: Once you are finished, use this tool.
- **Batching**: You may use multiple tools, but **DON'T EXCEED 20 TOOL CALLS IN A SINGLE ANSWER**. Focus on quality and grounding over quantity.

================================ Human Message =================================

Please update the Knowledge Graph based on the provided data.

### Input Text:
Gustav, 7th Prince of Sayn-Wittgenstein-Berleburg (Gustav Frederik Philip Richard; born 12 January 1969), is the eldest child and only son of Princess Benedikte of Denmark and Richard, 6th Prince of Sayn-Wittgenstein-Berleburg.
His first cousin is King Frederik X of Denmark.
Biography

Prince Gustav is the head of the House of Sayn-Wittgenstein-Berleburg, the senior branch of the formerly princely house of Sayn-Wittgenstein.
He resides at Schloss Berleburg-Wittgenstein in the town of Bad Berleburg, in North Rhine-Westphalia, Germany.
He is the son of Prince Richard of Sayn-Wittgenstein-Berleburg and Princess Benedikte of Denmark and has two sisters, Princess Alexandra of Sayn-Wittgenstein-Berleburg and Princess Nathalie of Sayn-Wittgenstein-Berleburg.
The principality and princely title of Sayn-Wittgenstein-Berleburg descended, historically, according to semi-Salic primogeniture.
If Gustav were to die without legitimate issue, the family heritage would devolve upon his father's younger brother, Prince Robin zu Sayn-Wittgenstein-Berleburg.
Gustav was formerly engaged to be married to Elvire Pasté de Rochefort (granddaughter of French Ambassador André Rodocanachi and wife Nada Diplarakou, herself sister of Aliki Diplarakou and grand-aunt of Princess Sibilla of Luxembourg); the engagement was announced on 16 August 2000 and the wedding planned for 12 May 2001 in Paris.
For many years, he resided with his partner, Carina Axelsson, although they were unable to marry due to a clause in Gustav's grandfather's will preventing him from inheriting family property if he marries someone not of Protestant, noble and Aryan descent.
However, on 27 April 2022, the Danish court confirmed that Gustav could marry Axelsson on 3 June 2022, civilly and on 4 June 2022, religiously in Bad Berleburg.
The couple's son, Prince Gustav Albrecht, was born on 26 May 2023 in the United States via surrogacy.
On 26 April 2024, the couple welcomed their second child, a girl, Princess Mafalda, also via surrogacy.
He is the godfather of Count Richard von Pfeil und Klein-Ellguth, son of his sister Alexandra; Konstantin Johannsmann, son of his second sister Nathalie; and Prince Vincent of Denmark, son of his first cousin, Frederik X.


Ancestry




References

External links



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix ns2: <http://www.w3.org/2003/11/swrl#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

: a owl:Ontology ;
    dcterms:source <http://www.co-ode.org/roberts/family-tree.owl> .

:alsoKnownAs a owl:AnnotationProperty .

:formerlyKnownAs a owl:AnnotationProperty .

:hasBirthYear a rdfs:Datatype,
        owl:AnnotationProperty .

:hasDeathYear a owl:AnnotationProperty .

:hasMarriageYear a owl:AnnotationProperty .

:isAuntOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isSisterOf :isParentOf ) .

:isUncleOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isBrotherOf :isParentOf ) .

:knownAs a owl:AnnotationProperty .

dcterms:source a owl:AnnotationProperty .

ns1:isRuleEnabled a owl:AnnotationProperty .

:hasBrother a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isBrotherOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasDaughter a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isDaughterOf .

:hasFather a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Man ;
    rdfs:subPropertyOf :hasParent ;
    owl:inverseOf :isFatherOf .

:hasMother a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Woman ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf ;
    owl:inverseOf :isMotherOf .

:hasSister a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isSisterOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasSon a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isSonOf .

:isBloodrelationOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty .

:isDaughterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:isFatherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isMotherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isSonOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:DomainEntity a owl:Class .

:Female a owl:Class ;
    rdfs:subClassOf :Sex ;
    owl:disjointWith :Male .

:hasAncestor a owl:ObjectProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty ;
    owl:inverseOf :isAncestorOf .

:isBrotherOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:Male a owl:Class ;
    rdfs:subClassOf :Sex .

:hasRelation a owl:ObjectProperty,
        owl:SymmetricProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person .

:hasSex a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Sex .

:isAncestorOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation .

:isSisterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf .

:hasChild a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:inverseOf :isChildOf .

:hasParent a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Person ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:equivalentProperty :isChildOf ;
    owl:inverseOf :isParentOf .

:isSiblingOf a owl:ObjectProperty,
        owl:SymmetricProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isBloodrelationOf ;
    owl:propertyChainAxiom ( :hasParent :isParentOf ) .

:Sex a owl:Class ;
    rdfs:subClassOf :DomainEntity ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Female :Male ) ] .

:isChildOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:propertyDisjointWith :isSisterOf .

:x a ns2:Variable .

:Man a owl:Class ;
    owl:disjointWith :Sex,
        :Woman ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Male ] ) ] .

:isParentOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:propertyDisjointWith :isSisterOf .

:Woman a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Female ] ) ] .

:y a ns2:Variable .

:Ancestor a owl:Class ;
    owl:disjointWith :Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :isAncestorOf ;
                        owl:someValuesFrom :Person ] ) ] .

:Person a owl:Class ;
    rdfs:subClassOf [ a owl:Restriction ;
            owl:onProperty :hasFather ;
            owl:someValuesFrom :Man ],
        [ a owl:Restriction ;
            owl:onProperty :hasMother ;
            owl:someValuesFrom :Woman ],
        [ a owl:Restriction ;
            owl:onProperty :hasSex ;
            owl:someValuesFrom :Sex ],
        [ a owl:Restriction ;
            owl:maxQualifiedCardinality "2"^^xsd:nonNegativeInteger ;
            owl:onClass :Person ;
            owl:onProperty :hasParent ],
        :DomainEntity ;
    owl:disjointWith :Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Man :Woman ) ] .

[] a ns2:Imp ;
    rdfs:label "infer hasSon" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasBrother" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasSister" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (a1c9a8a5-d321-4b5a-aa49-7f0e692a1b50)
 Call ID: a1c9a8a5-d321-4b5a-aa49-7f0e692a1b50
  Args:
    type: :Man
    source: Gustav_7th_Prince_of_Sayn-Wittgenstein-Berleburg
  AssignClass (a797b43a-4400-4213-8718-f1ae95fa97bd)
 Call ID: a797b43a-4400-4213-8718-f1ae95fa97bd
  Args:
    type: :Person
    source: Gustav_7th_Prince_of_Sayn-Wittgenstein-Berleburg
  AssignClass (818bc66e-7da6-426a-9b13-27ac52abb4d6)
 Call ID: 818bc66e-7da6-426a-9b13-27ac52abb4d6
  Args:
    type: :Woman
    source: Princess_Benedikte_of_Denmark
  AssignClass (d51b005f-7142-4631-9ff5-9780ef5a3333)
 Call ID: d51b005f-7142-4631-9ff5-9780ef5a3333
  Args:
    type: :Person
    source: Princess_Benedikte_of_Denmark
  AssignClass (62d3c073-6374-479c-a6c2-334ce5c762a4)
 Call ID: 62d3c073-6374-479c-a6c2-334ce5c762a4
  Args:
    type: :Man
    source: Richard_6th_Prince_of_Sayn-Wittgenstein-Berleburg
  AssignClass (cb51f600-d224-4db5-921f-219ccbe1a8b4)
 Call ID: cb51f600-d224-4db5-921f-219ccbe1a8b4
  Args:
    type: :Person
    source: Richard_6th_Prince_of_Sayn-Wittgenstein-Berleburg
  AddLiteral (c701ae8c-cc30-4cc2-9781-b21c6aa22fe8)
 Call ID: c701ae8c-cc30-4cc2-9781-b21c6aa22fe8
  Args:
    source: Gustav_7th_Prince_of_Sayn-Wittgenstein-Berleburg
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1969
  AddTriple (ada152f2-e283-4ad6-b7d1-d9bb5b1285fb)
 Call ID: ada152f2-e283-4ad6-b7d1-d9bb5b1285fb
  Args:
    target: Richard_6th_Prince_of_Sayn-Wittgenstein-Berleburg
    relation: :hasFather
    source: Gustav_7th_Prince_of_Sayn-Wittgenstein-Berleburg
  AddTriple (ee6f6024-c81c-4c0b-adb0-7abb41549d3e)
 Call ID: ee6f6024-c81c-4c0b-adb0-7abb41549d3e
  Args:
    source: Gustav_7th_Prince_of_Sayn-Wittgenstein-Berleburg
    target: Princess_Benedikte_of_Denmark
    relation: :hasMother
  AssignClass (dd048d3e-ee95-4d08-a633-e4cafd5e972f)
 Call ID: dd048d3e-ee95-4d08-a633-e4cafd5e972f
  Args:
    type: :Man
    source: King_Frederik_X_of_Denmark
  AssignClass (1fd07346-b9f9-4228-9077-5a0174610c9d)
 Call ID: 1fd07346-b9f9-4228-9077-5a0174610c9d
  Args:
    type: :Person
    source: King_Frederik_X_of_Denmark
  AddTriple (f81d654e-d46f-433c-b78d-ce890c669ff6)
 Call ID: f81d654e-d46f-433c-b78d-ce890c669ff6
  Args:
    source: Gustav_7th_Prince_of_Sayn-Wittgenstein-Berleburg
    relation: :isBloodrelationOf
    target: King_Frederik_X_of_Denmark
  AssignClass (49e1b8ea-7402-4e58-9d2d-05be45397fea)
 Call ID: 49e1b8ea-7402-4e58-9d2d-05be45397fea
  Args:
    type: :Woman
    source: Princess_Alexandra_of_Sayn-Wittgenstein-Berleburg
  AssignClass (e326c2f0-d46e-446e-a787-0c0ef036b1db)
 Call ID: e326c2f0-d46e-446e-a787-0c0ef036b1db
  Args:
    type: :Person
    source: Princess_Alexandra_of_Sayn-Wittgenstein-Berleburg
  AssignClass (614239cd-0561-4744-a6cc-e94111ab0ee0)
 Call ID: 614239cd-0561-4744-a6cc-e94111ab0ee0
  Args:
    type: :Woman
    source: Princess_Nathalie_of_Sayn-Wittgenstein-Berleburg
  AssignClass (0bb2c392-5224-4773-a856-5b5996e8fb4c)
 Call ID: 0bb2c392-5224-4773-a856-5b5996e8fb4c
  Args:
    type: :Person
    source: Princess_Nathalie_of_Sayn-Wittgenstein-Berleburg
  AddTriple (e9cc01c7-d7f6-41dc-9226-70759aade910)
 Call ID: e9cc01c7-d7f6-41dc-9226-70759aade910
  Args:
    source: Gustav_7th_Prince_of_Sayn-Wittgenstein-Berleburg
    relation: :hasSister
    target: Princess_Alexandra_of_Sayn-Wittgenstein-Berleburg
  AddTriple (c6465ac0-0ab8-4fe0-badf-cf5f28caea7f)
 Call ID: c6465ac0-0ab8-4fe0-badf-cf5f28caea7f
  Args:
    target: Princess_Nathalie_of_Sayn-Wittgenstein-Berleburg
    relation: :hasSister
    source: Gustav_7th_Prince_of_Sayn-Wittgenstein-Berleburg
  AssignClass (a6e00f7d-edee-47f4-9d4e-a1cae0990dbc)
 Call ID: a6e00f7d-edee-47f4-9d4e-a1cae0990dbc
  Args:
    type: :Man
    source: Prince_Robin_zu_Sayn-Wittgenstein-Berleburg
  AssignClass (5b936759-a849-488f-85ce-a680f5dedfbf)
 Call ID: 5b936759-a849-488f-85ce-a680f5dedfbf
  Args:
    type: :Person
    source: Prince_Robin_zu_Sayn-Wittgenstein-Berleburg
  AddTriple (b6f5a33f-f975-4f3e-bbb3-c111a1f2afb6)
 Call ID: b6f5a33f-f975-4f3e-bbb3-c111a1f2afb6
  Args:
    source: Richard_6th_Prince_of_Sayn-Wittgenstein-Berleburg
    target: Prince_Robin_zu_Sayn-Wittgenstein-Berleburg
    relation: :hasBrother
  AssignClass (468a39f7-50ef-4ff5-92aa-18dacd39c73d)
 Call ID: 468a39f7-50ef-4ff5-92aa-18dacd39c73d
  Args:
    type: :Woman
    source: Carina_Axelsson
  AssignClass (7b6b283a-09da-4597-b66b-208304235e18)
 Call ID: 7b6b283a-09da-4597-b66b-208304235e18
  Args:
    type: :Person
    source: Carina_Axelsson
  AssignClass (553dde18-527b-4ab5-999f-02f98bce8719)
 Call ID: 553dde18-527b-4ab5-999f-02f98bce8719
  Args:
    type: :Man
    source: Prince_Gustav_Albrecht
  AssignClass (2259bfdf-ebda-4931-8dc5-5dc6a4095d1f)
 Call ID: 2259bfdf-ebda-4931-8dc5-5dc6a4095d1f
  Args:
    type: :Person
    source: Prince_Gustav_Albrecht
  AddTriple (7316dafa-294c-42e0-8ad8-6541c958b6a9)
 Call ID: 7316dafa-294c-42e0-8ad8-6541c958b6a9
  Args:
    relation: :hasFather
    target: Gustav_7th_Prince_of_Sayn-Wittgenstein-Berleburg
    source: Prince_Gustav_Albrecht
  AddTriple (982f7d0e-afbf-48ac-8105-74ec1c03bdaf)
 Call ID: 982f7d0e-afbf-48ac-8105-74ec1c03bdaf
  Args:
    source: Prince_Gustav_Albrecht
    relation: :hasMother
    target: Carina_Axelsson
  AssignClass (db9aa0e5-3748-4551-ada5-81dd27346fcd)
 Call ID: db9aa0e5-3748-4551-ada5-81dd27346fcd
  Args:
    type: :Woman
    source: Princess_Mafalda
  AssignClass (8a76a9d7-1689-4f36-8e9e-83fe9a372ed9)
 Call ID: 8a76a9d7-1689-4f36-8e9e-83fe9a372ed9
  Args:
    type: :Person
    source: Princess_Mafalda
  AddTriple (98a50551-b3cf-4459-8d24-f34687de7771)
 Call ID: 98a50551-b3cf-4459-8d24-f34687de7771
  Args:
    source: Princess_Mafalda
    relation: :hasFather
    target: Gustav_7th_Prince_of_Sayn-Wittgenstein-Berleburg
  AddTriple (7ee4bdbf-12b6-41b4-8b05-7461b17a1752)
 Call ID: 7ee4bdbf-12b6-41b4-8b05-7461b17a1752
  Args:
    source: Princess_Mafalda
    target: Carina_Axelsson
    relation: :hasMother
  Finish (cbcbb176-a83a-40b4-98e9-6ba9e385b231)
 Call ID: cbcbb176-a83a-40b4-98e9-6ba9e385b231
  Args:
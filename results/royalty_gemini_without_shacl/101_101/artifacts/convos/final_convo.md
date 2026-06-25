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
@prefix ns1: <http://www.w3.org/2003/11/swrl#> .
@prefix ns2: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
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

ns2:isRuleEnabled a owl:AnnotationProperty .

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

:x a ns1:Variable .

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

:y a ns1:Variable .

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

[] a ns1:Imp ;
    rdfs:label "infer hasSon" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasBrother" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasSister" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (a5bf1efe-8733-44ec-b6df-a27b6903a85c)
 Call ID: a5bf1efe-8733-44ec-b6df-a27b6903a85c
  Args:
    source: Gustav_7th_Prince_of_Sayn-Wittgenstein-Berleburg
    type: :Man
  AssignClass (5be04fcd-e1c0-4b45-8508-abc4490c2bf7)
 Call ID: 5be04fcd-e1c0-4b45-8508-abc4490c2bf7
  Args:
    source: Princess_Benedikte_of_Denmark
    type: :Woman
  AssignClass (54623948-d86b-48b5-8b60-bb5bf82251f7)
 Call ID: 54623948-d86b-48b5-8b60-bb5bf82251f7
  Args:
    type: :Man
    source: Richard_6th_Prince_of_Sayn-Wittgenstein-Berleburg
  AssignClass (549ce78d-2cc6-4edb-a016-f5e241f946bc)
 Call ID: 549ce78d-2cc6-4edb-a016-f5e241f946bc
  Args:
    type: :Man
    source: King_Frederik_X_of_Denmark
  AssignClass (179b2e84-bbf0-43ed-9888-33c5f4d40f10)
 Call ID: 179b2e84-bbf0-43ed-9888-33c5f4d40f10
  Args:
    type: :Man
    source: Prince_Robin_zu_Sayn-Wittgenstein-Berleburg
  AssignClass (751e887f-7dbb-4f60-8fd5-a029b2d0526d)
 Call ID: 751e887f-7dbb-4f60-8fd5-a029b2d0526d
  Args:
    source: Carina_Axelsson
    type: :Woman
  AssignClass (33df30ad-25dc-4eea-87ff-295bc8e204e0)
 Call ID: 33df30ad-25dc-4eea-87ff-295bc8e204e0
  Args:
    source: Prince_Gustav_Albrecht
    type: :Man
  AssignClass (e49d9fb1-f2bd-4dbd-b2ca-e5f10ce5d1d7)
 Call ID: e49d9fb1-f2bd-4dbd-b2ca-e5f10ce5d1d7
  Args:
    type: :Woman
    source: Princess_Mafalda
  AssignClass (b06f3451-d021-49b0-b20e-cb7136fcac2a)
 Call ID: b06f3451-d021-49b0-b20e-cb7136fcac2a
  Args:
    source: Princess_Alexandra_of_Sayn-Wittgenstein-Berleburg
    type: :Woman
  AssignClass (f7805867-40d1-44e4-b1a8-0dd11062a026)
 Call ID: f7805867-40d1-44e4-b1a8-0dd11062a026
  Args:
    source: Princess_Nathalie_of_Sayn-Wittgenstein-Berleburg
    type: :Woman
  AssignClass (6aff72d0-08a3-422c-99aa-e7ffecd10015)
 Call ID: 6aff72d0-08a3-422c-99aa-e7ffecd10015
  Args:
    type: :Man
    source: Count_Richard_von_Pfeil_und_Klein-Ellguth
  AssignClass (a16d87b0-2a5a-40a9-bfe2-0bfd04444c1f)
 Call ID: a16d87b0-2a5a-40a9-bfe2-0bfd04444c1f
  Args:
    source: Konstantin_Johannsmann
    type: :Man
  AssignClass (92f09ba4-9f3d-4f54-afa3-5106f8613c69)
 Call ID: 92f09ba4-9f3d-4f54-afa3-5106f8613c69
  Args:
    source: Prince_Vincent_of_Denmark
    type: :Man
  AddLiteral (fc1e34cb-5b7d-4fa7-9705-4a6fed4ab657)
 Call ID: fc1e34cb-5b7d-4fa7-9705-4a6fed4ab657
  Args:
    source: Gustav_7th_Prince_of_Sayn-Wittgenstein-Berleburg
    literal_value: 1969
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddTriple (55303233-3c89-4701-a44a-2fe6bffe60b2)
 Call ID: 55303233-3c89-4701-a44a-2fe6bffe60b2
  Args:
    relation: :hasMother
    source: Gustav_7th_Prince_of_Sayn-Wittgenstein-Berleburg
    target: Princess_Benedikte_of_Denmark
  AddTriple (b0755b1a-f63b-4076-82ba-5421cb1d30eb)
 Call ID: b0755b1a-f63b-4076-82ba-5421cb1d30eb
  Args:
    relation: :hasFather
    source: Gustav_7th_Prince_of_Sayn-Wittgenstein-Berleburg
    target: Richard_6th_Prince_of_Sayn-Wittgenstein-Berleburg
  AddTriple (259e5184-757c-44b1-93cb-57a009618705)
 Call ID: 259e5184-757c-44b1-93cb-57a009618705
  Args:
    relation: :hasSister
    target: Princess_Alexandra_of_Sayn-Wittgenstein-Berleburg
    source: Gustav_7th_Prince_of_Sayn-Wittgenstein-Berleburg
  AddTriple (4e325fe6-c73d-445c-a0ed-a5d00669bc30)
 Call ID: 4e325fe6-c73d-445c-a0ed-a5d00669bc30
  Args:
    target: Princess_Nathalie_of_Sayn-Wittgenstein-Berleburg
    source: Gustav_7th_Prince_of_Sayn-Wittgenstein-Berleburg
    relation: :hasSister
  AddTriple (15e7ae67-2a68-402c-8110-52a042279227)
 Call ID: 15e7ae67-2a68-402c-8110-52a042279227
  Args:
    relation: :isBrotherOf
    source: Richard_6th_Prince_of_Sayn-Wittgenstein-Berleburg
    target: Prince_Robin_zu_Sayn-Wittgenstein-Berleburg
  AddTriple (fa1276b4-d7db-41f0-a1b9-1a27af5e2059)
 Call ID: fa1276b4-d7db-41f0-a1b9-1a27af5e2059
  Args:
    target: Carina_Axelsson
    source: Prince_Gustav_Albrecht
    relation: :hasMother
  AddTriple (9383fde4-d45f-487b-aeb2-1f4f5d7b01ba)
 Call ID: 9383fde4-d45f-487b-aeb2-1f4f5d7b01ba
  Args:
    target: Gustav_7th_Prince_of_Sayn-Wittgenstein-Berleburg
    source: Prince_Gustav_Albrecht
    relation: :hasFather
  AddTriple (303745ac-1ad3-44df-af06-af9afc45d008)
 Call ID: 303745ac-1ad3-44df-af06-af9afc45d008
  Args:
    relation: :hasMother
    target: Carina_Axelsson
    source: Princess_Mafalda
  AddTriple (f54647b0-1978-442a-a6be-947eab3e313d)
 Call ID: f54647b0-1978-442a-a6be-947eab3e313d
  Args:
    source: Princess_Mafalda
    target: Gustav_7th_Prince_of_Sayn-Wittgenstein-Berleburg
    relation: :hasFather
  AddTriple (08f41885-387f-4327-87e9-9a83c1ad4fde)
 Call ID: 08f41885-387f-4327-87e9-9a83c1ad4fde
  Args:
    relation: :hasMother
    source: Count_Richard_von_Pfeil_und_Klein-Ellguth
    target: Princess_Alexandra_of_Sayn-Wittgenstein-Berleburg
  AddTriple (79b134a4-505e-49ff-ad47-43602d0bfc88)
 Call ID: 79b134a4-505e-49ff-ad47-43602d0bfc88
  Args:
    target: Princess_Nathalie_of_Sayn-Wittgenstein-Berleburg
    source: Konstantin_Johannsmann
    relation: :hasMother
  AddTriple (e42694fd-786b-4c7e-adf4-64ca4dc92e2d)
 Call ID: e42694fd-786b-4c7e-adf4-64ca4dc92e2d
  Args:
    source: Prince_Vincent_of_Denmark
    target: King_Frederik_X_of_Denmark
    relation: :hasFather
  Finish (868a20b1-ef94-4f58-877a-ec1cbabb9d17)
 Call ID: 868a20b1-ef94-4f58-877a-ec1cbabb9d17
  Args:
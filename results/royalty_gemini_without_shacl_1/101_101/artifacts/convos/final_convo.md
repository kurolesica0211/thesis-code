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
  AssignClass (014fb398-6195-466e-8c19-c9ebe1fe4b57)
 Call ID: 014fb398-6195-466e-8c19-c9ebe1fe4b57
  Args:
    type: :Man
    source: Gustav_7th_Prince_of_Sayn-Wittgenstein-Berleburg
  AssignClass (5c1747c3-6c8f-4705-b5fd-fc43e1aada2f)
 Call ID: 5c1747c3-6c8f-4705-b5fd-fc43e1aada2f
  Args:
    type: :Person
    source: Gustav_7th_Prince_of_Sayn-Wittgenstein-Berleburg
  AddLiteral (9f73b948-cba3-43e2-ad91-650b780cede5)
 Call ID: 9f73b948-cba3-43e2-ad91-650b780cede5
  Args:
    relation: :knownAs
    literal_value: Gustav Frederik Philip Richard
    source: Gustav_7th_Prince_of_Sayn-Wittgenstein-Berleburg
    literal_type: xsd:string
  AddLiteral (be4cf6d5-1385-4765-b8e0-268a77b6c095)
 Call ID: be4cf6d5-1385-4765-b8e0-268a77b6c095
  Args:
    literal_type: xsd:integer
    source: Gustav_7th_Prince_of_Sayn-Wittgenstein-Berleburg
    literal_value: 1969
    relation: :hasBirthYear
  AssignClass (d2c28813-8325-4edf-a21d-570f5df032ae)
 Call ID: d2c28813-8325-4edf-a21d-570f5df032ae
  Args:
    type: :Woman
    source: Princess_Benedikte_of_Denmark
  AssignClass (196ab86d-8bef-464b-8361-0661b0c244c5)
 Call ID: 196ab86d-8bef-464b-8361-0661b0c244c5
  Args:
    type: :Person
    source: Princess_Benedikte_of_Denmark
  AssignClass (aa0d6967-1986-48ae-adb6-ef9e497707cd)
 Call ID: aa0d6967-1986-48ae-adb6-ef9e497707cd
  Args:
    type: :Man
    source: Richard_6th_Prince_of_Sayn-Wittgenstein-Berleburg
  AssignClass (5a2bc40a-787e-4d87-96a7-2f3248a565ed)
 Call ID: 5a2bc40a-787e-4d87-96a7-2f3248a565ed
  Args:
    type: :Person
    source: Richard_6th_Prince_of_Sayn-Wittgenstein-Berleburg
  AddTriple (c9ef84c1-e302-4612-b2a6-402be30843d2)
 Call ID: c9ef84c1-e302-4612-b2a6-402be30843d2
  Args:
    relation: :hasMother
    source: Gustav_7th_Prince_of_Sayn-Wittgenstein-Berleburg
    target: Princess_Benedikte_of_Denmark
  AddTriple (ea3f4a19-3ec8-477d-a7fb-c4e1a2a5746a)
 Call ID: ea3f4a19-3ec8-477d-a7fb-c4e1a2a5746a
  Args:
    target: Richard_6th_Prince_of_Sayn-Wittgenstein-Berleburg
    relation: :hasFather
    source: Gustav_7th_Prince_of_Sayn-Wittgenstein-Berleburg
  AssignClass (221d3ddc-e819-4617-81c8-edda7f5bcfcc)
 Call ID: 221d3ddc-e819-4617-81c8-edda7f5bcfcc
  Args:
    type: :Man
    source: King_Frederik_X_of_Denmark
  AssignClass (8ae6b27a-a677-422f-9f4a-56598eeacea0)
 Call ID: 8ae6b27a-a677-422f-9f4a-56598eeacea0
  Args:
    type: :Person
    source: King_Frederik_X_of_Denmark
  AssignClass (01f79007-1484-46da-a6db-ade2b8c0edb3)
 Call ID: 01f79007-1484-46da-a6db-ade2b8c0edb3
  Args:
    type: :Woman
    source: Princess_Alexandra_of_Sayn-Wittgenstein-Berleburg
  AssignClass (ebd8106c-352c-46da-aba6-20eb5e97d1bb)
 Call ID: ebd8106c-352c-46da-aba6-20eb5e97d1bb
  Args:
    type: :Person
    source: Princess_Alexandra_of_Sayn-Wittgenstein-Berleburg
  AssignClass (46b7f20a-e44a-4169-aa3b-894b4fa6b8bd)
 Call ID: 46b7f20a-e44a-4169-aa3b-894b4fa6b8bd
  Args:
    type: :Woman
    source: Princess_Nathalie_of_Sayn-Wittgenstein-Berleburg
  AssignClass (16453348-decc-4acc-9c9b-13a728be5c86)
 Call ID: 16453348-decc-4acc-9c9b-13a728be5c86
  Args:
    type: :Person
    source: Princess_Nathalie_of_Sayn-Wittgenstein-Berleburg
  AddTriple (24f80126-c513-47f4-bccd-9d771dbe2362)
 Call ID: 24f80126-c513-47f4-bccd-9d771dbe2362
  Args:
    source: Gustav_7th_Prince_of_Sayn-Wittgenstein-Berleburg
    relation: :isSiblingOf
    target: Princess_Alexandra_of_Sayn-Wittgenstein-Berleburg
  AddTriple (7538e4c5-668c-4bd6-9a47-00c6c80a9817)
 Call ID: 7538e4c5-668c-4bd6-9a47-00c6c80a9817
  Args:
    target: Princess_Nathalie_of_Sayn-Wittgenstein-Berleburg
    source: Gustav_7th_Prince_of_Sayn-Wittgenstein-Berleburg
    relation: :isSiblingOf
  AssignClass (4556df33-b98d-4910-b6d8-f162c4d08983)
 Call ID: 4556df33-b98d-4910-b6d8-f162c4d08983
  Args:
    type: :Man
    source: Prince_Robin_zu_Sayn-Wittgenstein-Berleburg
  AssignClass (7202768a-8552-4fb8-a02d-7ec9ae5f60a1)
 Call ID: 7202768a-8552-4fb8-a02d-7ec9ae5f60a1
  Args:
    type: :Person
    source: Prince_Robin_zu_Sayn-Wittgenstein-Berleburg
  AddTriple (13a94def-b945-4777-8957-5c27780cf913)
 Call ID: 13a94def-b945-4777-8957-5c27780cf913
  Args:
    source: Richard_6th_Prince_of_Sayn-Wittgenstein-Berleburg
    relation: :isBrotherOf
    target: Prince_Robin_zu_Sayn-Wittgenstein-Berleburg
  AssignClass (1720810d-fe07-4ba1-9c77-53d774b8397a)
 Call ID: 1720810d-fe07-4ba1-9c77-53d774b8397a
  Args:
    type: :Woman
    source: Carina_Axelsson
  AssignClass (46c0229c-b8a8-4093-b2a9-66abf5883379)
 Call ID: 46c0229c-b8a8-4093-b2a9-66abf5883379
  Args:
    type: :Person
    source: Carina_Axelsson
  AssignClass (e68bc566-c617-46cb-beb2-fdab051bc761)
 Call ID: e68bc566-c617-46cb-beb2-fdab051bc761
  Args:
    type: :Man
    source: Prince_Gustav_Albrecht
  AssignClass (f3f2bde3-c580-4ba1-89ab-9277629cd093)
 Call ID: f3f2bde3-c580-4ba1-89ab-9277629cd093
  Args:
    type: :Person
    source: Prince_Gustav_Albrecht
  AddTriple (b2283a9e-2cb1-4e8e-977b-5f56b8bb3fd0)
 Call ID: b2283a9e-2cb1-4e8e-977b-5f56b8bb3fd0
  Args:
    source: Prince_Gustav_Albrecht
    relation: :hasFather
    target: Gustav_7th_Prince_of_Sayn-Wittgenstein-Berleburg
  AddTriple (c3af940c-b990-42ae-af8c-4b218ae672bb)
 Call ID: c3af940c-b990-42ae-af8c-4b218ae672bb
  Args:
    target: Carina_Axelsson
    source: Prince_Gustav_Albrecht
    relation: :hasMother
  AssignClass (9b6ed61e-5790-4bc8-8b11-2c2e8319e3b4)
 Call ID: 9b6ed61e-5790-4bc8-8b11-2c2e8319e3b4
  Args:
    type: :Woman
    source: Princess_Mafalda
  AssignClass (82a79df5-795a-47da-b99f-82f98988d4eb)
 Call ID: 82a79df5-795a-47da-b99f-82f98988d4eb
  Args:
    type: :Person
    source: Princess_Mafalda
  AddTriple (b7b0d237-2ae6-40f7-a046-d8e6d7ce1f80)
 Call ID: b7b0d237-2ae6-40f7-a046-d8e6d7ce1f80
  Args:
    source: Princess_Mafalda
    relation: :hasFather
    target: Gustav_7th_Prince_of_Sayn-Wittgenstein-Berleburg
  AddTriple (e6c3633f-0bda-4cfe-8d63-67c365c1276b)
 Call ID: e6c3633f-0bda-4cfe-8d63-67c365c1276b
  Args:
    source: Princess_Mafalda
    relation: :hasMother
    target: Carina_Axelsson
  AssignClass (3e013db1-ebd7-4bd7-ac16-5b61aeed840d)
 Call ID: 3e013db1-ebd7-4bd7-ac16-5b61aeed840d
  Args:
    type: :Man
    source: Count_Richard_von_Pfeil_und_Klein-Ellguth
  AssignClass (e27427d1-0baa-49b5-a558-f741fde036fa)
 Call ID: e27427d1-0baa-49b5-a558-f741fde036fa
  Args:
    type: :Person
    source: Count_Richard_von_Pfeil_und_Klein-Ellguth
  AddTriple (a053751f-4eec-4824-8ba8-60c42125c8a2)
 Call ID: a053751f-4eec-4824-8ba8-60c42125c8a2
  Args:
    relation: :hasMother
    source: Count_Richard_von_Pfeil_und_Klein-Ellguth
    target: Princess_Alexandra_of_Sayn-Wittgenstein-Berleburg
  AssignClass (1c54e9ad-e69a-4f63-9d5c-4ce8e47b981e)
 Call ID: 1c54e9ad-e69a-4f63-9d5c-4ce8e47b981e
  Args:
    type: :Man
    source: Konstantin_Johannsmann
  AssignClass (ca7742fe-593a-41e0-8e59-75e83c9a328d)
 Call ID: ca7742fe-593a-41e0-8e59-75e83c9a328d
  Args:
    type: :Person
    source: Konstantin_Johannsmann
  AddTriple (80fd6b4e-53c9-4f79-aa0c-a49fda900a9b)
 Call ID: 80fd6b4e-53c9-4f79-aa0c-a49fda900a9b
  Args:
    relation: :hasMother
    source: Konstantin_Johannsmann
    target: Princess_Nathalie_of_Sayn-Wittgenstein-Berleburg
  AssignClass (01722e4c-4115-4be4-82bc-72db7037e45f)
 Call ID: 01722e4c-4115-4be4-82bc-72db7037e45f
  Args:
    type: :Man
    source: Prince_Vincent_of_Denmark
  AssignClass (1ccebf3d-c401-4476-bc42-62ebcd45bfe0)
 Call ID: 1ccebf3d-c401-4476-bc42-62ebcd45bfe0
  Args:
    type: :Person
    source: Prince_Vincent_of_Denmark
  AddTriple (0049b65a-2a91-4081-89b2-7fc4f0cec512)
 Call ID: 0049b65a-2a91-4081-89b2-7fc4f0cec512
  Args:
    relation: :hasFather
    source: Prince_Vincent_of_Denmark
    target: King_Frederik_X_of_Denmark
  Finish (daa45b59-8e5a-46f3-9f71-864f82a577d5)
 Call ID: daa45b59-8e5a-46f3-9f71-864f82a577d5
  Args:
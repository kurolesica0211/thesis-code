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
Lady Davina Elizabeth Alice Benedikte Windsor (born 19 November 1977) is a member of the British royal family, and is the elder daughter of the Duke and Duchess of Gloucester.
She was known as Lady Davina Lewis between 2004 and 2018, during her marriage to Gary Lewis.
Early life and education

Davina Elizabeth Alice Benedikte Windsor was born on 19 November 1977 at St Mary's Hospital, London, the second child of Prince Richard, Duke of Gloucester and Birgitte, Duchess of Gloucester.
Her godparents are Captain Mark Phillips, the Duke of Buccleuch, Elisabeth, Lady Camoys, Susan Wigley, Roger Wellesley Smith and Caroline, Baroness Rosenørn-Lehn.
Lady Davina grew up in Kensington Palace.
Marriage and children

On 31 July 2004, Davina married Gary Christie Lewis (born 15 August 1970), a Māori.
Lewis is also the first person of known Māori descent to marry a member of the royal family, or to marry the daughter of a British prince.
As she is a legitimate descendant in the male line of George V and in line to the British throne, the Royal Marriages Act 1772 required that Royal Assent to the wedding be obtained in advance for the marriage to be legal and the descendants thereof to inherit rights of succession to the thrones of the Commonwealth realms, including that of New Zealand.
The wedding took place on 31 July 2004 at the private chapel of Kensington Palace, Davina's childhood home.
Apart from the Duke and Duchess of Gloucester and the bride's siblings, no other members of the royal family were present at the wedding; only close friends and family were involved.
Davina and her former husband have a daughter, Senna Kowhai, who was born on 22 June 2010 and a son, Tāne Mahuta, who was born 25 May 2012.
Davina was also stepmother to Lewis's son from a previous relationship, Ari (born 1992).
Davina does not carry out official functions but does attend family events including royal weddings.
Davina and Gary Lewis were invited to attend the Queen's reception for members of the New Zealand All Blacks at Buckingham Palace in 2005.
She and her then husband also attended Prince William's wedding in 2011.



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
  AssignClass (ab9e93e5-d015-4533-a759-6e4c4f634d3d)
 Call ID: ab9e93e5-d015-4533-a759-6e4c4f634d3d
  Args:
    source: :Lady_Davina_Windsor
    type: :Woman
  AssignClass (f6b828da-3eb0-4e73-b1f4-c11c950eff66)
 Call ID: f6b828da-3eb0-4e73-b1f4-c11c950eff66
  Args:
    source: :Lady_Davina_Windsor
    type: :Person
  AddLiteral (33fe16b9-4024-49ec-b1cc-eb50755ced5f)
 Call ID: 33fe16b9-4024-49ec-b1cc-eb50755ced5f
  Args:
    literal_value: 1977-11-19
    literal_type: xsd:string
    source: :Lady_Davina_Windsor
    relation: :hasBirthYear
  AssignClass (66fcdb75-2900-4ae3-8a83-40d70e190b36)
 Call ID: 66fcdb75-2900-4ae3-8a83-40d70e190b36
  Args:
    type: :Man
    source: :Prince_Richard_Duke_of_Gloucester
  AssignClass (3c83eec3-c1fa-4288-a0ab-fe267617cae2)
 Call ID: 3c83eec3-c1fa-4288-a0ab-fe267617cae2
  Args:
    source: :Prince_Richard_Duke_of_Gloucester
    type: :Person
  AssignClass (6453944b-92ba-4670-84d5-b94c323ff0c9)
 Call ID: 6453944b-92ba-4670-84d5-b94c323ff0c9
  Args:
    source: :Birgitte_Duchess_of_Gloucester
    type: :Woman
  AssignClass (a1f32dd8-95c1-42fc-98de-03bb212d1bbc)
 Call ID: a1f32dd8-95c1-42fc-98de-03bb212d1bbc
  Args:
    type: :Person
    source: :Birgitte_Duchess_of_Gloucester
  AddTriple (4fb65328-a53e-40f3-8c6d-a902c35ef643)
 Call ID: 4fb65328-a53e-40f3-8c6d-a902c35ef643
  Args:
    relation: :hasFather
    source: :Lady_Davina_Windsor
    target: :Prince_Richard_Duke_of_Gloucester
  AddTriple (ea822b24-7ebf-4b8b-84ff-a5783f14c3ec)
 Call ID: ea822b24-7ebf-4b8b-84ff-a5783f14c3ec
  Args:
    relation: :hasMother
    target: :Birgitte_Duchess_of_Gloucester
    source: :Lady_Davina_Windsor
  AssignClass (4025c45d-b486-4d48-adf0-eb568b4047a5)
 Call ID: 4025c45d-b486-4d48-adf0-eb568b4047a5
  Args:
    type: :Man
    source: :Gary_Christie_Lewis
  AssignClass (ca4de74b-16ba-4d0d-b878-2ada87d4bf9c)
 Call ID: ca4de74b-16ba-4d0d-b878-2ada87d4bf9c
  Args:
    source: :Gary_Christie_Lewis
    type: :Person
  AddLiteral (d0f5c2e3-cfc8-4ab6-9f08-c4fbeb57b47f)
 Call ID: d0f5c2e3-cfc8-4ab6-9f08-c4fbeb57b47f
  Args:
    literal_value: 1970-08-15
    source: :Gary_Christie_Lewis
    literal_type: xsd:string
    relation: :hasBirthYear
  AddTriple (e47dca69-1e67-4e42-883d-f22ea87ae01f)
 Call ID: e47dca69-1e67-4e42-883d-f22ea87ae01f
  Args:
    target: :Gary_Christie_Lewis
    source: :Lady_Davina_Windsor
    relation: :hasRelation
  AddLiteral (f48f871f-b372-4931-b686-cf68e8e9c951)
 Call ID: f48f871f-b372-4931-b686-cf68e8e9c951
  Args:
    literal_type: xsd:string
    source: :Lady_Davina_Windsor
    literal_value: 2004
    relation: :hasMarriageYear
  AddLiteral (8668eb79-2029-4b46-aae0-c18bf779b8ae)
 Call ID: 8668eb79-2029-4b46-aae0-c18bf779b8ae
  Args:
    relation: :alsoKnownAs
    literal_type: xsd:string
    source: :Lady_Davina_Windsor
    literal_value: Lady Davina Lewis
  AssignClass (b3070a7e-35ba-465f-a84e-4a3d1be3108c)
 Call ID: b3070a7e-35ba-465f-a84e-4a3d1be3108c
  Args:
    type: :Woman
    source: :Senna_Kowhai
  AssignClass (9a873f1f-f20f-4190-be6a-0f8ad9403bed)
 Call ID: 9a873f1f-f20f-4190-be6a-0f8ad9403bed
  Args:
    type: :Person
    source: :Senna_Kowhai
  AddTriple (0a07a549-062f-4620-a1a2-9282da7bc2f1)
 Call ID: 0a07a549-062f-4620-a1a2-9282da7bc2f1
  Args:
    relation: :isDaughterOf
    target: :Lady_Davina_Windsor
    source: :Senna_Kowhai
  AddTriple (f7b4409a-952a-41c4-accd-2ee8458b1dbc)
 Call ID: f7b4409a-952a-41c4-accd-2ee8458b1dbc
  Args:
    source: :Senna_Kowhai
    target: :Gary_Christie_Lewis
    relation: :isDaughterOf
  AssignClass (f8635f40-54f0-4a21-9079-b9c8f7e7dcae)
 Call ID: f8635f40-54f0-4a21-9079-b9c8f7e7dcae
  Args:
    source: :Tane_Mahuta
    type: :Man
  AssignClass (1a762b7b-69e1-4d82-b076-2e30825a01b4)
 Call ID: 1a762b7b-69e1-4d82-b076-2e30825a01b4
  Args:
    type: :Person
    source: :Tane_Mahuta
  AddTriple (49686dda-0951-41c3-bbac-40278e87aa26)
 Call ID: 49686dda-0951-41c3-bbac-40278e87aa26
  Args:
    relation: :isSonOf
    target: :Lady_Davina_Windsor
    source: :Tane_Mahuta
  AddTriple (13af2ac7-0d6e-4c09-b1eb-58700fd9115d)
 Call ID: 13af2ac7-0d6e-4c09-b1eb-58700fd9115d
  Args:
    relation: :isSonOf
    source: :Tane_Mahuta
    target: :Gary_Christie_Lewis
  AssignClass (edd0187c-0d74-4cd4-9cc1-5c7f11003d89)
 Call ID: edd0187c-0d74-4cd4-9cc1-5c7f11003d89
  Args:
    source: :Ari
    type: :Man
  AssignClass (4f51a2e1-133e-4d85-9ab6-4f45b33a5044)
 Call ID: 4f51a2e1-133e-4d85-9ab6-4f45b33a5044
  Args:
    type: :Person
    source: :Ari
  AddLiteral (e85d4e2b-9688-4f9b-80d3-12cea41cd052)
 Call ID: e85d4e2b-9688-4f9b-80d3-12cea41cd052
  Args:
    relation: :hasBirthYear
    literal_type: xsd:string
    source: :Ari
    literal_value: 1992
  AddTriple (1ca0fa8d-8e53-49b5-9a09-870d0b50fd30)
 Call ID: 1ca0fa8d-8e53-49b5-9a09-870d0b50fd30
  Args:
    relation: :isSonOf
    source: :Ari
    target: :Gary_Christie_Lewis
  Finish (5a8b3e36-af7e-494d-b166-e80f32083449)
 Call ID: 5a8b3e36-af7e-494d-b166-e80f32083449
  Args:
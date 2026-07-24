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
Princess Nuria


Princess Françoise


Princess Mariam


Princess Monique


Prince Juan Jorge de Bagration-Mukhrani (born 18 August 1977) is a Spanish-born Georgian prince and member of the House of Mukhrani of the Bagrationi dynasty and a distant relation to the Spanish royal family.
Early life and family

Prince Juan Jorge de Bagration-Mukhrani was born on 18 August 1977 in Madrid to Prince Bagrat de Bagration y de Baviera and Doña María del Carmen de Ulloa y Suelves.
His paternal grandfather, Prince Irakli Bagration of Mukhrani, was exiled from Georgia during the invasion of the Red Army, living in Germany, Italy, and finally settling in Spain.
His paternal grandmother, Infanta María de las Mercedes of Spain was a member of the Spanish royal family and the German House of Wittelsbach; she was the daughter of Prince Ferdinand of Bavaria, granddaughter of Alfonso XII of Spain, and niece of Alfonso XIII of Spain.
His maternal grandfather was Gonzalo Maria de Ulloa y Ramírez de Haro, Marqués de Castro-Serna, Count de Adanero.
Prince Juan's parents divorced in 2005 and his father remarried in 2009 to Françoise Cazaudehore.
Prince Juan is a member of the House of Mukhrani, a branch of the Bagrationi dynasty that ruled Georgia from the Middle Ages until the nineteenth century, when Georgia was annexed into the Russian Empire.
Prince Juan studied at Collège Alpin International Beau Soleil, a boarding school in Villars-sur-Ollon, Switzerland and was a schoolmate and childhood friend of Cayetano Rivera Ordóñez.
Personal life

Prince Juan met Kristine Dzidziguri, a Georgian model, in 2014.
They were married a few months later in a civil ceremony on 10 May 2014 in Ronda, Spain.
The couple began planning a religious ceremony but were delayed due to social and political conflicts within Georgia and because of Prince Juan's father's declining health.
On 2 June 2018, Prince Juan and Dzidziguri received a blessing from Ilia II of Georgia, the Catholicos-Patriarch of All Georgia.
Their wedding reception was held at the Palace of Mukhrani.
Later during their Indonesian tour, Prince Juan and Princess Kristine attended a gala lunch focused on establishing a cultural relationship between Indonesia and Georgia.
Prince Juan is the founder of the Georgian Foundation, a non-profit organization that promotes Georgian culture.
In October 2019 he launched a wine brand called Prince Ioane Bagrationi wines.



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
  AssignClass (74a35aeb-1dad-4423-af36-c9741370d10a)
 Call ID: 74a35aeb-1dad-4423-af36-c9741370d10a
  Args:
    type: :Man
    source: Prince_Juan_Jorge_de_Bagration-Mukhrani
  AssignClass (ededc4d1-3720-4b76-86f4-d3d1df2e486d)
 Call ID: ededc4d1-3720-4b76-86f4-d3d1df2e486d
  Args:
    type: :Person
    source: Prince_Juan_Jorge_de_Bagration-Mukhrani
  AddLiteral (b09036e5-ca17-4c7a-9429-e479e485f9e5)
 Call ID: b09036e5-ca17-4c7a-9429-e479e485f9e5
  Args:
    relation: :hasBirthYear
    literal_value: 1977
    literal_type: xsd:integer
    source: Prince_Juan_Jorge_de_Bagration-Mukhrani
  AssignClass (c50a42c6-0189-49b6-bac3-d57be51db745)
 Call ID: c50a42c6-0189-49b6-bac3-d57be51db745
  Args:
    type: :Man
    source: Prince_Bagrat_de_Bagration_y_de_Baviera
  AssignClass (88b2a641-450b-4633-a480-2b15406c4275)
 Call ID: 88b2a641-450b-4633-a480-2b15406c4275
  Args:
    type: :Person
    source: Prince_Bagrat_de_Bagration_y_de_Baviera
  AssignClass (e24ce113-2150-4ae4-a683-51f7632d9d60)
 Call ID: e24ce113-2150-4ae4-a683-51f7632d9d60
  Args:
    type: :Woman
    source: Doña_María_del_Carmen_de_Ulloa_y_Suelves
  AssignClass (041241fb-26ea-48a5-acd4-b7a47964c03c)
 Call ID: 041241fb-26ea-48a5-acd4-b7a47964c03c
  Args:
    type: :Person
    source: Doña_María_del_Carmen_de_Ulloa_y_Suelves
  AddTriple (b39e6b69-83b0-4c68-a846-301ea92ce0f0)
 Call ID: b39e6b69-83b0-4c68-a846-301ea92ce0f0
  Args:
    relation: :hasFather
    target: Prince_Bagrat_de_Bagration_y_de_Baviera
    source: Prince_Juan_Jorge_de_Bagration-Mukhrani
  AddTriple (50f057c6-4556-4f0a-a859-d3b69390b9ce)
 Call ID: 50f057c6-4556-4f0a-a859-d3b69390b9ce
  Args:
    relation: :hasMother
    target: Doña_María_del_Carmen_de_Ulloa_y_Suelves
    source: Prince_Juan_Jorge_de_Bagration-Mukhrani
  AssignClass (5db7cc1c-343b-4c3e-ae60-7691d339354e)
 Call ID: 5db7cc1c-343b-4c3e-ae60-7691d339354e
  Args:
    source: Prince_Irakli_Bagration_of_Mukhrani
    type: :Man
  AssignClass (140d9b43-c458-422a-9e95-dc2529295b1b)
 Call ID: 140d9b43-c458-422a-9e95-dc2529295b1b
  Args:
    type: :Person
    source: Prince_Irakli_Bagration_of_Mukhrani
  AddTriple (2c2a5251-59c2-4dcc-8e21-25544a9607b8)
 Call ID: 2c2a5251-59c2-4dcc-8e21-25544a9607b8
  Args:
    source: Prince_Bagrat_de_Bagration_y_de_Baviera
    target: Prince_Irakli_Bagration_of_Mukhrani
    relation: :hasFather
  AssignClass (aaf5be6c-6782-4b99-86c7-0ce6b3d990fb)
 Call ID: aaf5be6c-6782-4b99-86c7-0ce6b3d990fb
  Args:
    source: Infanta_María_de_las_Mercedes_of_Spain
    type: :Woman
  AssignClass (b3fa5d03-81d6-4b3f-b6ba-c665f611bb10)
 Call ID: b3fa5d03-81d6-4b3f-b6ba-c665f611bb10
  Args:
    source: Infanta_María_de_las_Mercedes_of_Spain
    type: :Person
  AddTriple (fb83bc72-3880-4135-ad4d-d828958d0d76)
 Call ID: fb83bc72-3880-4135-ad4d-d828958d0d76
  Args:
    relation: :hasMother
    target: Infanta_María_de_las_Mercedes_of_Spain
    source: Prince_Bagrat_de_Bagration_y_de_Baviera
  AssignClass (fa104fc3-9d3a-4293-a010-aa1d03f7db4e)
 Call ID: fa104fc3-9d3a-4293-a010-aa1d03f7db4e
  Args:
    source: Prince_Ferdinand_of_Bavaria
    type: :Man
  AssignClass (cef6c388-ce42-44c4-ad42-0313376de2bf)
 Call ID: cef6c388-ce42-44c4-ad42-0313376de2bf
  Args:
    type: :Person
    source: Prince_Ferdinand_of_Bavaria
  AddTriple (7f036724-2081-4b12-baee-33188740231f)
 Call ID: 7f036724-2081-4b12-baee-33188740231f
  Args:
    relation: :hasFather
    source: Infanta_María_de_las_Mercedes_of_Spain
    target: Prince_Ferdinand_of_Bavaria
  AssignClass (d5612bda-4df1-4389-8f92-166ca8b1f72c)
 Call ID: d5612bda-4df1-4389-8f92-166ca8b1f72c
  Args:
    type: :Man
    source: Alfonso_XII_of_Spain
  AssignClass (09112e1b-fe2c-44b5-9f02-9f4da3c7253e)
 Call ID: 09112e1b-fe2c-44b5-9f02-9f4da3c7253e
  Args:
    type: :Person
    source: Alfonso_XII_of_Spain
  AssignClass (2fcd3a27-1ee4-42ca-a4b1-02724cf645f0)
 Call ID: 2fcd3a27-1ee4-42ca-a4b1-02724cf645f0
  Args:
    source: Alfonso_XIII_of_Spain
    type: :Man
  AssignClass (e18bfb0c-8bc8-4994-9982-303f854f9773)
 Call ID: e18bfb0c-8bc8-4994-9982-303f854f9773
  Args:
    source: Alfonso_XIII_of_Spain
    type: :Person
  AssignClass (1bc73ccc-f970-4e62-985c-00bf3fb0b84d)
 Call ID: 1bc73ccc-f970-4e62-985c-00bf3fb0b84d
  Args:
    source: Gonzalo_Maria_de_Ulloa_y_Ramírez_de_Haro
    type: :Man
  AssignClass (71af8e8a-3538-4c0e-9b92-e3985e175b1b)
 Call ID: 71af8e8a-3538-4c0e-9b92-e3985e175b1b
  Args:
    type: :Person
    source: Gonzalo_Maria_de_Ulloa_y_Ramírez_de_Haro
  AddTriple (e96b4e0c-bf96-4159-bd47-808f39402781)
 Call ID: e96b4e0c-bf96-4159-bd47-808f39402781
  Args:
    relation: :hasFather
    target: Gonzalo_Maria_de_Ulloa_y_Ramírez_de_Haro
    source: Doña_María_del_Carmen_de_Ulloa_y_Suelves
  AssignClass (2c0e1776-078e-43e4-a8a5-1045efd3ce77)
 Call ID: 2c0e1776-078e-43e4-a8a5-1045efd3ce77
  Args:
    source: Françoise_Cazaudehore
    type: :Woman
  AssignClass (ebafbec1-d88f-47d3-bbf9-6a2045ebecea)
 Call ID: ebafbec1-d88f-47d3-bbf9-6a2045ebecea
  Args:
    source: Françoise_Cazaudehore
    type: :Person
  AssignClass (ef119111-11fa-4349-b991-e576ae0ef1ab)
 Call ID: ef119111-11fa-4349-b991-e576ae0ef1ab
  Args:
    source: Kristine_Dzidziguri
    type: :Woman
  AssignClass (f9ddf63c-cd93-46a9-bd73-b6dbb125a966)
 Call ID: f9ddf63c-cd93-46a9-bd73-b6dbb125a966
  Args:
    source: Kristine_Dzidziguri
    type: :Person
  AddLiteral (0765bf28-9cc2-47c5-8f21-7e3ecd350eab)
 Call ID: 0765bf28-9cc2-47c5-8f21-7e3ecd350eab
  Args:
    source: Prince_Juan_Jorge_de_Bagration-Mukhrani
    literal_value: 2014
    literal_type: xsd:integer
    relation: :hasMarriageYear
  AddTriple (6010cff8-0952-42bd-8f65-ac83b521dfcf)
 Call ID: 6010cff8-0952-42bd-8f65-ac83b521dfcf
  Args:
    relation: :hasRelation
    target: Kristine_Dzidziguri
    source: Prince_Juan_Jorge_de_Bagration-Mukhrani
  AssignClass (129d8dba-c9a7-4858-90f4-188cd448aed4)
 Call ID: 129d8dba-c9a7-4858-90f4-188cd448aed4
  Args:
    type: :Man
    source: Ilia_II_of_Georgia
  AssignClass (1bfa6ffc-9da7-4919-ad86-aec85949f1d6)
 Call ID: 1bfa6ffc-9da7-4919-ad86-aec85949f1d6
  Args:
    source: Ilia_II_of_Georgia
    type: :Person
  Finish (a06cfc32-212c-4141-bf8d-8d7b8115c69f)
 Call ID: a06cfc32-212c-4141-bf8d-8d7b8115c69f
  Args:
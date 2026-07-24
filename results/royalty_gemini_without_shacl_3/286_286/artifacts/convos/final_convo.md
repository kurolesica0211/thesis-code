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
Rafael of Orléans-Braganza (Portuguese: Rafael de Orléans e Bragança; born 24 April 1986) is a member of the Imperial House of Brazil.
He is the heir presumptive to his childless uncle, Prince Bertrand, the current head of the Vassouras branch of the House of Orléans-Braganza and one of the claimants to the defunct Brazilian Throne.
Rafael became heir presumptive following the death of his father, Prince Antônio, in November 2024.
Family

Born in Petrópolis, Brazil on 26 April 1986, he is the third child and second son of Prince Antônio de Orleans e Bragança and Princess Christine of Ligne.
He has an older brother and sister, Prince Pedro Luiz and Princess Amélia and a younger sister, Princess Maria Gabriela.
His name in full is Rafael Antonio Maria José Francisco Miguel Gabriel Gonzaga de Orléans e Bragança e Ligne.
His paternal grandparents were Prince Pedro Henrique of Orléans-Bragança, one of two claimants to be head of the Brazilian Imperial House, and Princess Maria Elisabeth of Bavaria.
His maternal grandparents were Antoine, 13th Prince of Ligne, and Princess Alix of Luxembourg.
His mother's family, the House of Ligne, is one of the oldest and most prominent Wallonian noble families still extant in Belgium.
Christine is a niece of Grand Duke Jean, who reigned in Luxembourg until his abdication in 2000.
Personal life

Rafael has a degree in manufacturing engineering from Pontifical Catholic University of Rio de Janeiro, working at the InBev subsidiary in London.
Rafael also has a partnership and a tourism enterprise with headquarters in New York, Paris and Rio de Janeiro.
Rafael has expressed in statements his desire to marry a princess who is part of "Catholic royalty or high nobility".
Appointments

In February 2022, after the floods that devastated the city of Petrópolis, Rafael came to the aid of the victims, bringing them essential goods that the imperial house received from monarchist supporters.
Honors

Genealogy

Ancestry

Patrilineal descent

Rafael is a member of the House of Orléans-Braganza, a sub-branch of the House of Bourbon, itself a branch of the House of Capet and of the Robertians.
Rafael's patriline is the line from which he is descended father to son.
It follows the Dukes of Orléans, the Kings of France, the Dukes and Counts of Vendôme, the Counts of La Marche, the first Duke of Bourbon, a Count of Clermont, and before them, again the Kings of France.



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
  AssignClass (dbe7ba80-db52-495a-8288-5085fc2295c2)
 Call ID: dbe7ba80-db52-495a-8288-5085fc2295c2
  Args:
    source: :Rafael_of_Orleans-Braganza
    type: :Man
  AssignClass (1280f7f2-7d37-4ae9-8f9d-7c6b4401e199)
 Call ID: 1280f7f2-7d37-4ae9-8f9d-7c6b4401e199
  Args:
    source: :Rafael_of_Orleans-Braganza
    type: :Person
  AddLiteral (0614578b-6de3-4adf-b5fb-f751a33d6312)
 Call ID: 0614578b-6de3-4adf-b5fb-f751a33d6312
  Args:
    literal_value: 1986
    source: :Rafael_of_Orleans-Braganza
    literal_type: xsd:integer
    relation: :hasBirthYear
  AssignClass (5f8b6cb0-8898-43a1-96c9-6c4cf71a03cd)
 Call ID: 5f8b6cb0-8898-43a1-96c9-6c4cf71a03cd
  Args:
    source: :Prince_Bertrand
    type: :Man
  AssignClass (6a8a2dee-9110-45ce-98ac-44940b24db80)
 Call ID: 6a8a2dee-9110-45ce-98ac-44940b24db80
  Args:
    source: :Prince_Bertrand
    type: :Person
  AddTriple (30499169-469b-4653-8691-8e9632a5cc35)
 Call ID: 30499169-469b-4653-8691-8e9632a5cc35
  Args:
    relation: :hasRelation
    source: :Rafael_of_Orleans-Braganza
    target: :Prince_Bertrand
  AssignClass (2c3551cf-10f7-4a1e-818d-7d7f541540a3)
 Call ID: 2c3551cf-10f7-4a1e-818d-7d7f541540a3
  Args:
    source: :Prince_Antonio
    type: :Man
  AssignClass (1d3ab140-55dd-498d-98cc-066152bcd2bb)
 Call ID: 1d3ab140-55dd-498d-98cc-066152bcd2bb
  Args:
    source: :Prince_Antonio
    type: :Person
  AddTriple (c3567058-da81-41c0-9336-e8952d971349)
 Call ID: c3567058-da81-41c0-9336-e8952d971349
  Args:
    target: :Prince_Antonio
    source: :Rafael_of_Orleans-Braganza
    relation: :hasFather
  AddLiteral (5e29c5a9-6ff8-44f5-a182-0ea4a7e4ed0c)
 Call ID: 5e29c5a9-6ff8-44f5-a182-0ea4a7e4ed0c
  Args:
    source: :Prince_Antonio
    literal_type: xsd:integer
    literal_value: 2024
    relation: :hasDeathYear
  AssignClass (08df23c6-9b01-42ff-803c-8782a163033c)
 Call ID: 08df23c6-9b01-42ff-803c-8782a163033c
  Args:
    source: :Princess_Christine_of_Ligne
    type: :Woman
  AssignClass (8ccf2955-50c8-4e58-b5ef-c1585f15c823)
 Call ID: 8ccf2955-50c8-4e58-b5ef-c1585f15c823
  Args:
    source: :Princess_Christine_of_Ligne
    type: :Person
  AddTriple (61697df7-f660-46f7-8551-8a9bb5d93649)
 Call ID: 61697df7-f660-46f7-8551-8a9bb5d93649
  Args:
    target: :Princess_Christine_of_Ligne
    source: :Rafael_of_Orleans-Braganza
    relation: :hasMother
  AssignClass (3a34380b-54cc-443c-a3c2-4928c79637c6)
 Call ID: 3a34380b-54cc-443c-a3c2-4928c79637c6
  Args:
    type: :Man
    source: :Prince_Pedro_Luiz
  AssignClass (787672ee-59fd-42fe-bbf1-784d36d3df3c)
 Call ID: 787672ee-59fd-42fe-bbf1-784d36d3df3c
  Args:
    source: :Prince_Pedro_Luiz
    type: :Person
  AddTriple (c1d0afef-60cb-456d-bdcb-586278c858a7)
 Call ID: c1d0afef-60cb-456d-bdcb-586278c858a7
  Args:
    relation: :isSiblingOf
    target: :Prince_Pedro_Luiz
    source: :Rafael_of_Orleans-Braganza
  AssignClass (a195c62e-c20c-4280-91bc-e195b781ae08)
 Call ID: a195c62e-c20c-4280-91bc-e195b781ae08
  Args:
    source: :Princess_Amelia
    type: :Woman
  AssignClass (dd67cf14-9983-4c76-8cc2-cb3c3bfb030f)
 Call ID: dd67cf14-9983-4c76-8cc2-cb3c3bfb030f
  Args:
    type: :Person
    source: :Princess_Amelia
  AddTriple (2782b1d0-c7a4-4058-a13e-a8b9571c114d)
 Call ID: 2782b1d0-c7a4-4058-a13e-a8b9571c114d
  Args:
    source: :Rafael_of_Orleans-Braganza
    target: :Princess_Amelia
    relation: :isSiblingOf
  AssignClass (c471fa8d-c128-4c34-8fad-120ae62388a6)
 Call ID: c471fa8d-c128-4c34-8fad-120ae62388a6
  Args:
    source: :Princess_Maria_Gabriela
    type: :Woman
  AssignClass (8a362dcc-b085-48a6-84b5-6795b37cf8b4)
 Call ID: 8a362dcc-b085-48a6-84b5-6795b37cf8b4
  Args:
    type: :Person
    source: :Princess_Maria_Gabriela
  AddTriple (2f7218a2-7fd0-4487-a11c-eac8d839ad9b)
 Call ID: 2f7218a2-7fd0-4487-a11c-eac8d839ad9b
  Args:
    source: :Rafael_of_Orleans-Braganza
    target: :Princess_Maria_Gabriela
    relation: :isSiblingOf
  AssignClass (427e3828-f488-45df-82aa-e1d840146d40)
 Call ID: 427e3828-f488-45df-82aa-e1d840146d40
  Args:
    source: :Prince_Pedro_Henrique_of_Orleans-Braganza
    type: :Man
  AssignClass (ff0cf26a-a1f7-4391-a7fb-a0b03035bae1)
 Call ID: ff0cf26a-a1f7-4391-a7fb-a0b03035bae1
  Args:
    type: :Person
    source: :Prince_Pedro_Henrique_of_Orleans-Braganza
  AddTriple (966fbbb0-e9e4-4aa9-a7dc-16588d9a0275)
 Call ID: 966fbbb0-e9e4-4aa9-a7dc-16588d9a0275
  Args:
    source: :Prince_Antonio
    target: :Prince_Pedro_Henrique_of_Orleans-Braganza
    relation: :hasFather
  AssignClass (0ea21527-9da7-4660-a309-485cfed3e819)
 Call ID: 0ea21527-9da7-4660-a309-485cfed3e819
  Args:
    source: :Princess_Maria_Elisabeth_of_Bavaria
    type: :Woman
  AssignClass (744911da-f667-485c-94a4-dbfccf64f799)
 Call ID: 744911da-f667-485c-94a4-dbfccf64f799
  Args:
    type: :Person
    source: :Princess_Maria_Elisabeth_of_Bavaria
  AddTriple (d3001b31-af20-415e-b1ef-2a5a0e361595)
 Call ID: d3001b31-af20-415e-b1ef-2a5a0e361595
  Args:
    relation: :hasMother
    source: :Prince_Antonio
    target: :Princess_Maria_Elisabeth_of_Bavaria
  AssignClass (198fdc07-5aef-4933-bc12-0f8ebf1ba210)
 Call ID: 198fdc07-5aef-4933-bc12-0f8ebf1ba210
  Args:
    type: :Man
    source: :Antoine_13th_Prince_of_Ligne
  AssignClass (6a034e66-fa92-4e6d-a94c-8dde546cbd3e)
 Call ID: 6a034e66-fa92-4e6d-a94c-8dde546cbd3e
  Args:
    type: :Person
    source: :Antoine_13th_Prince_of_Ligne
  AddTriple (b592c2d3-46a5-4d28-81e5-01c9fe4376c2)
 Call ID: b592c2d3-46a5-4d28-81e5-01c9fe4376c2
  Args:
    source: :Princess_Christine_of_Ligne
    target: :Antoine_13th_Prince_of_Ligne
    relation: :hasFather
  AssignClass (46dc943a-07c3-4369-95a1-3fb7127beb97)
 Call ID: 46dc943a-07c3-4369-95a1-3fb7127beb97
  Args:
    source: :Princess_Alix_of_Luxembourg
    type: :Woman
  AssignClass (0010359d-7e88-4e28-9a2a-c99bb3dc38d8)
 Call ID: 0010359d-7e88-4e28-9a2a-c99bb3dc38d8
  Args:
    source: :Princess_Alix_of_Luxembourg
    type: :Person
  AddTriple (06fc86a4-399e-42f2-a56c-0630ee811c98)
 Call ID: 06fc86a4-399e-42f2-a56c-0630ee811c98
  Args:
    relation: :hasMother
    source: :Princess_Christine_of_Ligne
    target: :Princess_Alix_of_Luxembourg
  AssignClass (56b46773-7bfe-4f18-abc5-f92da4b5c833)
 Call ID: 56b46773-7bfe-4f18-abc5-f92da4b5c833
  Args:
    type: :Man
    source: :Grand_Duke_Jean
  AssignClass (b73464fe-d31f-4314-9698-fd0562f2a9fc)
 Call ID: b73464fe-d31f-4314-9698-fd0562f2a9fc
  Args:
    source: :Grand_Duke_Jean
    type: :Person
  Finish (27a3ede0-9bbc-4b9d-953f-74dd8c241ff3)
 Call ID: 27a3ede0-9bbc-4b9d-953f-74dd8c241ff3
  Args:
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
Leopold IV, Prince of Lippe (Leopold Julius Bernhard Adalbert Otto Karl Gustav; 30 May 1871 – 30 December 1949) was the final sovereign of the Principality of Lippe in northwestern Germany from 1905 until his abdication in 1918.
He was the first and only ruler of Lippe of the Lippe-Biesterfeld branch.
Early life

He was born as Count Leopold of Lippe-Biesterfeld in Oberkassel, the son of Ernest, Count of Lippe-Biesterfeld and Countess Karoline of Wartensleben.
Leopold belonged to the Lippe-Biesterfeld line of the House of Lippe which was the most senior line of the princely house after the reigning Lippe-Detmold line.
Ruler of Lippe

Since 1895, the Principality of Lippe had been ruled by a regent due to the incapacity of Prince Alexander.
Leopold's father had acted as regent since 1897, and following his death on 26 September 1904, Leopold assumed the regency.
This was not recognized by the German Emperor Wilhelm II, who initially refused to legally recognize Leopold as regent as there was an issue over whether Leopold and his siblings were of legitimate rank, and as such eligible for the succession.
As a result, the Diet of Lippe appointed a high commission to consider the matter.
The regency issue was still ongoing when Prince Alexander died on 13 January 1905.
Leopold was confirmed as Prince of Lippe and Alexander's successor on 25 October 1905, following a court ruling.
On 3 June 1911, while out motoring, Leopold and his brother Prince Julius were attacked by a gang of Italian laborers who hurled a shower of missiles at the princes.
Though Leopold escaped unhurt, his brother received a head wound.
During World War I, Leopold upgraded the titles of the various lines of the House of Lippe.
One of the members to benefit from the granting of titles was Leopold's nephew Count Bernhard of Biesterfeld (son of Leopold's brother Bernhard), who would go on to become the Prince Consort of Queen Juliana of the Netherlands.
On 24 February 1916, Bernhard and his brother were upgraded to the title Prince of Lippe-Biesterfeld with the style Serene Highness.
The Counts of Lippe-Weissenfeld also benefited with creations of the title Prince of Lippe-Weissenfeld, with the style Serene Highness, taking place on 24 February 1916 for Count Clemens and his descendants, and again on 9 November 1918 for the other members of this line.
Just three days after upgrading the titles of members of the Lippe-Weissenfeld line, and following the German Empire's defeat in World War I and the subsequent revolution, Leopold was forced to renounce the throne on 12 November 1918.
Following the end of his rule, the Principality of Lippe was transformed into a Free state in the new Weimar Republic.
His eldest son the Hereditary Prince Ernst is reported to have been the first German prince to join the party when he signed up in May 1928.
In addition to being pro Nazi, both Hereditary Prince Ernst and Prince Chlodwig had contracted unequal marriages.
So in 1947 when Leopold wrote his will, Armin, his youngest son and only child with his second wife, would succeed him as head of the House of Lippe and also become administrator of the princely family's properties such as Schloss Detmold.
Thus when Leopold died in Detmold his three eldest sons were all disinherited and his youngest son Armin became head of the princely house.
Marriages and children

Leopold was married to Princess Bertha of Hesse-Philippsthal-Barchfeld (1874–1919) on 16 August 1901 in Rotenburg.



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
  AssignClass (6022c100-8720-4c6d-bb17-c69e2f01386e)
 Call ID: 6022c100-8720-4c6d-bb17-c69e2f01386e
  Args:
    source: Leopold_IV_Prince_of_Lippe
    type: :Man
  AddLiteral (ab8408d9-68ea-4e2d-aadd-ed690325e301)
 Call ID: ab8408d9-68ea-4e2d-aadd-ed690325e301
  Args:
    relation: :hasBirthYear
    literal_value: 1871
    source: Leopold_IV_Prince_of_Lippe
    literal_type: xsd:integer
  AddLiteral (8eed1a34-130e-49d5-8d71-86d4d682d0db)
 Call ID: 8eed1a34-130e-49d5-8d71-86d4d682d0db
  Args:
    source: Leopold_IV_Prince_of_Lippe
    literal_type: xsd:integer
    literal_value: 1949
    relation: :hasDeathYear
  AssignClass (05a59324-b06b-4817-bc52-eef552676df7)
 Call ID: 05a59324-b06b-4817-bc52-eef552676df7
  Args:
    source: Ernest_Count_of_Lippe-Biesterfeld
    type: :Man
  AssignClass (5960dab8-18bc-4442-8f5d-784af2a18c25)
 Call ID: 5960dab8-18bc-4442-8f5d-784af2a18c25
  Args:
    source: Karoline_of_Wartensleben
    type: :Woman
  AddTriple (fc11f217-6aa8-434c-8ae2-bc8241f31f02)
 Call ID: fc11f217-6aa8-434c-8ae2-bc8241f31f02
  Args:
    relation: :hasFather
    target: Ernest_Count_of_Lippe-Biesterfeld
    source: Leopold_IV_Prince_of_Lippe
  AddTriple (85dab78a-a386-4f81-9652-0dd4e96f9162)
 Call ID: 85dab78a-a386-4f81-9652-0dd4e96f9162
  Args:
    relation: :hasMother
    target: Karoline_of_Wartensleben
    source: Leopold_IV_Prince_of_Lippe
  AssignClass (43e0c5c5-55c3-4bf8-bce8-a2b08d55b695)
 Call ID: 43e0c5c5-55c3-4bf8-bce8-a2b08d55b695
  Args:
    source: Julius_Prince_of_Lippe
    type: :Man
  AddTriple (68101d22-2fe7-4035-b4dd-c86bd87691f8)
 Call ID: 68101d22-2fe7-4035-b4dd-c86bd87691f8
  Args:
    source: Leopold_IV_Prince_of_Lippe
    target: Julius_Prince_of_Lippe
    relation: :hasBrother
  AssignClass (68bbf785-7219-43dc-915b-62c56fe41ab8)
 Call ID: 68bbf785-7219-43dc-915b-62c56fe41ab8
  Args:
    type: :Man
    source: Bernhard_brother_of_Leopold
  AddTriple (ede25319-6030-4165-8b30-7aefc04d3539)
 Call ID: ede25319-6030-4165-8b30-7aefc04d3539
  Args:
    relation: :hasBrother
    source: Leopold_IV_Prince_of_Lippe
    target: Bernhard_brother_of_Leopold
  AssignClass (95397b7e-af0d-47fc-95b1-a6ed065292b1)
 Call ID: 95397b7e-af0d-47fc-95b1-a6ed065292b1
  Args:
    source: Bernhard_of_Biesterfeld_nephew
    type: :Man
  AddTriple (abcfdff6-b874-462a-be42-f633b8a75ea4)
 Call ID: abcfdff6-b874-462a-be42-f633b8a75ea4
  Args:
    target: Bernhard_brother_of_Leopold
    source: Bernhard_of_Biesterfeld_nephew
    relation: :hasFather
  AssignClass (112eb220-8317-44ec-93e2-cd017264a955)
 Call ID: 112eb220-8317-44ec-93e2-cd017264a955
  Args:
    source: Ernst_Hereditary_Prince
    type: :Man
  AddTriple (b0dc8f71-40e3-48c3-84b5-fa714aa8bd43)
 Call ID: b0dc8f71-40e3-48c3-84b5-fa714aa8bd43
  Args:
    relation: :hasFather
    source: Ernst_Hereditary_Prince
    target: Leopold_IV_Prince_of_Lippe
  AssignClass (7db9cfa1-e99c-4ae1-8279-b1138ecab2fe)
 Call ID: 7db9cfa1-e99c-4ae1-8279-b1138ecab2fe
  Args:
    type: :Man
    source: Chlodwig_Prince
  AddTriple (8d3ad4ae-7def-4c83-a8ed-d245e3516a87)
 Call ID: 8d3ad4ae-7def-4c83-a8ed-d245e3516a87
  Args:
    relation: :hasFather
    target: Leopold_IV_Prince_of_Lippe
    source: Chlodwig_Prince
  AssignClass (24205b95-3f24-42d1-9e4a-f5154cfd627b)
 Call ID: 24205b95-3f24-42d1-9e4a-f5154cfd627b
  Args:
    source: Armin_Prince
    type: :Man
  AddTriple (fed1ff5a-9861-48bb-bbb1-eaa84c3374fe)
 Call ID: fed1ff5a-9861-48bb-bbb1-eaa84c3374fe
  Args:
    relation: :hasFather
    target: Leopold_IV_Prince_of_Lippe
    source: Armin_Prince
  AssignClass (9c03fea0-57e5-4ea6-9cb0-28ae2b17edbc)
 Call ID: 9c03fea0-57e5-4ea6-9cb0-28ae2b17edbc
  Args:
    type: :Woman
    source: Bertha_of_Hesse-Philippsthal-Barchfeld
  AddLiteral (753c1817-8fa9-4ada-ad12-ee229c1adb18)
 Call ID: 753c1817-8fa9-4ada-ad12-ee229c1adb18
  Args:
    literal_type: xsd:integer
    source: Leopold_IV_Prince_of_Lippe
    literal_value: 1901
    relation: :hasMarriageYear
  AddTriple (b106f218-84b1-46f9-9c4e-559bac5d87bd)
 Call ID: b106f218-84b1-46f9-9c4e-559bac5d87bd
  Args:
    relation: :hasRelation
    target: Bertha_of_Hesse-Philippsthal-Barchfeld
    source: Leopold_IV_Prince_of_Lippe
  AddLiteral (91566fd4-cbcd-44b6-aed5-bbff2e6f2337)
 Call ID: 91566fd4-cbcd-44b6-aed5-bbff2e6f2337
  Args:
    literal_value: 1874
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Bertha_of_Hesse-Philippsthal-Barchfeld
  AddLiteral (1e80df22-0871-4c36-ac11-a93f2d91bdda)
 Call ID: 1e80df22-0871-4c36-ac11-a93f2d91bdda
  Args:
    literal_type: xsd:integer
    source: Bertha_of_Hesse-Philippsthal-Barchfeld
    literal_value: 1919
    relation: :hasDeathYear
  Finish (7d0565ba-d85b-48fa-b200-0f098f67c85d)
 Call ID: 7d0565ba-d85b-48fa-b200-0f098f67c85d
  Args:
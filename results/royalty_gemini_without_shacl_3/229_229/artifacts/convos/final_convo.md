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
Henri Philippe Pierre Marie d'Orléans (14 June 1933 – 21 January 2019) was the Orléanist pretender to the defunct French throne as Henry VII.
Henri was a retired military officer as well as an author and painter.
Early life

He was the first son of Henri, Count of Paris (1908–1999), and his wife Princess Isabelle of Orléans-Braganza, and was born in Woluwe-Saint-Pierre, Belgium, a law in 1886 having permanently exiled from France the heads of its formerly reigning dynasties and their eldest sons.
Despite the ban, while living in Belgium Henri occasionally accompanied his mother on brief visits to France and, later, to his mother's relatives in Brazil.
While his father sought to play a role in the French resistance, Henri, in 1940 a child of 7, remained at Larache with his mother, siblings, grandmother and father's sisters' families during the Nazi occupation of France, sharing a small desert home that lacked electricity.
Advised by Henri Giraud's Moroccan command that the Orléans had become unwelcome in the protectorate following the assassination of Vichy regime collaborater François Darlan by the monarchist Fernand Bonnier de La Chapelle, the family relocated to Pamplona in Spain until 1947, when they took up residence at the Quinta do Anjinho, an estate near Sintra, on the Portuguese Riviera.
During that year, President Vincent Auriol allowed Henri and his brother François to visit France, and in 1948 he was allowed to enroll in a lycée in Bordeaux.
The law of exile was abrogated in 1950, allowing Henri to repatriate with his parents.
Later that year, his parents purchased an estate near Paris, the Manoir du Cœur-Volant in Louveciennes, which became Henri's first home in France.
Henri studied at the Institut d'Études Politiques de Paris (Sciences Po), obtaining his bac in 1957, and on 30 June of that year, his father conferred upon him, as the heir apparent of his house, the title of "Count of Clermont", by which he was generally known during his father's lifetime.
Career

From October 1959 to April 1962, Henri worked at the Secretariat-General for National Defence and Security as a member of the French Foreign Legion.
Returning to civilian life in 1967, Henri and his family briefly occupied the Blanche Neige pavilion on the grounds of his father's Cœur-Volant estate before renting an apartment of their own in the 15th arrondissement of Paris.
Henri wrote several books, including:


Henri was also a painter and launched his own brand of perfume.
Marriages and children

Henri met Duchess Marie Therese of Württemberg (born 1934), like himself a descendant of King Louis-Philippe, at a ball given by the Thurn and Taxis family in Munich.
Five children were born from this union:


In 1984, Henri and Marie-Thérèse were divorced.
On 31 October 1984 Henri entered a civil marriage with Micaëla Anna María Cousiño y Quiñones de León (1938–2022), daughter of Luis Cousiño y Sebire and his wife, Antonia Maria Quiñones de Léon y Bañuelos, 4th Marquesa de San Carlos, and who had previously been divorced from Jean-Robert Bœuf.
For remarrying without consent, Henri's father initially declared him disinherited, substituting the non-dynastic title Comte de Mortain for his son's Clermont countship (the latter once held in appanage by a son of Louis IX of France, who became ancestor of the Bourbon-Orléans line).
Henri, though, refused all mail addressed to him as "Mortain".
On 27 February 1984 Marie-Thérèse, the former Countess of Clermont, was granted the title Duchess of Montpensier by her father-in-law.
On 11 February 1989 Henri was informed, by a hand-delivered letter written by his former wife, of the engagement of their eldest child Marie, to Prince Gundakar of Liechtenstein, a cousin of the ruler of that principality, the wedding date being set for 29 July 1989.
Although Henri acknowledged, in a 12 May 1989 Point de Vue interview, that it had been three years since he had seen Marie, he and his second wife, Micaëla Cousiño, had been welcomed for the first time to the home of his mother, the Countess of Paris, that day: Henri further acknowledged to the press that, Marie having written to invite him to her wedding, he looked forward to conducting her to the altar, rumours to the contrary notwithstanding.
At the engagement party held the next day at the Palais Pallavicini, the Vienna home of the fiancé's parents, photographs were taken, and would later be published, showing Henri speaking cordially with his daughter, sons, former wife and future son-in-law.
However, it was on this occasion that Henri learned that he would not be escorting Marie to her bridegroom during the wedding.
Meanwhile, Marie-Thérèse had sent out invitations to the wedding in her name alone, omitting not only mention of Marie's father, but also of her grandfather, Monseigneur the Count of Paris who, until then, had largely sided with the Duchess of Montpensier in family matters and had consented to his granddaughter's choice of a spouse.
Henri and his father refused to attend the wedding but Marie proceeded to marry civilly at Dreux's city hall on 22 July 1989, and religiously at the castle of her mother's brother in Germany, on 29 July 1989.
All but two of Henri's eight siblings also boycotted the ceremonies, but his sister Diane (wife of Montpensier's brother) hosted, and Henri's mother, Madame the Countess of Paris, was a guest at the religious wedding.
Tensions lessened after several years, and on 7 March 1991 Henri's father reinstated him as heir apparent and Count of Clermont, simultaneously giving Micaëla the title "Princesse de Joinville".
In 1980, Henri joined the Grand Orient de France where he became Grand Master of the regular Masonic Lodge "Lys de France" No 1297.
Head of house

Until he succeeded his father as royal claimant, Henri and his second wife occupied an apartment in Paris.
On 19 June 1999, Henri's father died and he became the new head of the House of Orléans.
He took the traditional title, Count of Paris, adding an ancient one, Duke of France, not borne by his Orléans or Bourbon forebears, but used a thousand years ago by his ancestors, before Hugh Capet took the title of king.
His wife assumed the title "Duchess of France", deferring to the continued use of "Countess of Paris" by Henri's widowed mother until her death on 5 July 2003, whereupon Micaela assumed that title.
After his father's death, Henri annulled his father's decision to deprive his brothers Michel (Count of Évreux) and Thibaut (the late Count of La Marche) of their succession rights because Michel married a French noblewoman without permission and because Thibaut married a commoner.
He also bestowed titles upon the sons of his brother Prince Jacques, Duke of Orléans: Prince Charles-Louis d'Orléans, Duke of Chartres (born 1972), and Prince Foulques d'Orléans, Duke of Aumale and Count of Eu (born 1974).
Henri recognised his disabled eldest son François as his dynastic heir-apparent, with the title Count of Clermont, declaring that François would exercise his prerogatives as head of the dynasty under the "regency" of his younger brother Prince Jean, Duke of Vendôme.
In 2009, Henri obtained an annulment of his marriage to Marie-Thérèse of Württemberg from the Holy See.
As Count of Paris, Henri took part in some European royal events attending, for instance, the 2011 marriage of Albert II of Monaco.
Legal cases

Prior to succeeding his father as royal claimant, Henri launched an unsuccessful court case (1987–1989) in which he challenged the right of his rival paternal 10th cousin Louis-Alphonse, Duke of Anjou, to use the undifferenced royal arms of France and the Anjou title.
The French courts dismissed the case on the grounds that Henri failed to prove that he had demonstrated a right to the hereditaments in questions, noting also that the court lacked jurisdiction in a dispute over dynastic claims of France's former royal family.
In 2000 bailiffs pursued Henri for US$143,000 back rent after he fled the Villa Boileau, a 17th-century Paris house he had occupied.



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
  AssignClass (877f6a6f-2880-4939-8971-37a862d8e0e9)
 Call ID: 877f6a6f-2880-4939-8971-37a862d8e0e9
  Args:
    type: :Man
    source: :Henri_dOrleans
  AssignClass (c77ef7c0-ab32-476a-8c76-5ce91d95f5c6)
 Call ID: c77ef7c0-ab32-476a-8c76-5ce91d95f5c6
  Args:
    source: :Henri_dOrleans
    type: :Person
  AddLiteral (ccfb2d7e-f319-45ba-bfd1-d1dba01b026d)
 Call ID: ccfb2d7e-f319-45ba-bfd1-d1dba01b026d
  Args:
    literal_type: xsd:integer
    source: :Henri_dOrleans
    literal_value: 1933
    relation: :hasBirthYear
  AddLiteral (548fc555-539f-4965-a919-69b001546c39)
 Call ID: 548fc555-539f-4965-a919-69b001546c39
  Args:
    relation: :hasDeathYear
    source: :Henri_dOrleans
    literal_value: 2019
    literal_type: xsd:integer
  AssignClass (17d3f17c-c5bd-46d7-ae7c-877a0234433b)
 Call ID: 17d3f17c-c5bd-46d7-ae7c-877a0234433b
  Args:
    type: :Man
    source: :Henri_Count_of_Paris_1908
  AssignClass (3b1e48b7-c947-45fa-b0d0-a16530936f1e)
 Call ID: 3b1e48b7-c947-45fa-b0d0-a16530936f1e
  Args:
    source: :Henri_Count_of_Paris_1908
    type: :Person
  AddLiteral (f8d5ee88-4514-405e-a173-f2b3fc66a29b)
 Call ID: f8d5ee88-4514-405e-a173-f2b3fc66a29b
  Args:
    literal_type: xsd:integer
    source: :Henri_Count_of_Paris_1908
    literal_value: 1908
    relation: :hasBirthYear
  AddLiteral (3b78adf0-e12a-4b2a-98ea-41245a1ead7e)
 Call ID: 3b78adf0-e12a-4b2a-98ea-41245a1ead7e
  Args:
    literal_value: 1999
    source: :Henri_Count_of_Paris_1908
    relation: :hasDeathYear
    literal_type: xsd:integer
  AssignClass (69119ef5-b2a0-4192-8b0c-107ad68798ae)
 Call ID: 69119ef5-b2a0-4192-8b0c-107ad68798ae
  Args:
    type: :Woman
    source: :Isabelle_of_Orleans_Braganza
  AssignClass (2222b7ec-8350-4670-bade-5288d81ddb1e)
 Call ID: 2222b7ec-8350-4670-bade-5288d81ddb1e
  Args:
    type: :Person
    source: :Isabelle_of_Orleans_Braganza
  AddTriple (7715cee0-0084-42bb-a998-7d479088bc3d)
 Call ID: 7715cee0-0084-42bb-a998-7d479088bc3d
  Args:
    relation: :hasFather
    source: :Henri_dOrleans
    target: :Henri_Count_of_Paris_1908
  AddTriple (683d6106-bb4c-4908-b8ce-72d9393c70bc)
 Call ID: 683d6106-bb4c-4908-b8ce-72d9393c70bc
  Args:
    target: :Isabelle_of_Orleans_Braganza
    relation: :hasMother
    source: :Henri_dOrleans
  AssignClass (5e447542-0c4b-4304-bae1-16fe28eb9c0c)
 Call ID: 5e447542-0c4b-4304-bae1-16fe28eb9c0c
  Args:
    source: :Francois_dOrleans
    type: :Man
  AssignClass (ee6e150a-a37a-49ad-86e7-3a1b60164ca8)
 Call ID: ee6e150a-a37a-49ad-86e7-3a1b60164ca8
  Args:
    source: :Francois_dOrleans
    type: :Person
  AddTriple (ccef634f-312a-4156-8fe9-0597ecb84992)
 Call ID: ccef634f-312a-4156-8fe9-0597ecb84992
  Args:
    source: :Francois_dOrleans
    relation: :isBrotherOf
    target: :Henri_dOrleans
  AssignClass (42cf3327-7384-4475-85af-f7054edc44fe)
 Call ID: 42cf3327-7384-4475-85af-f7054edc44fe
  Args:
    type: :Woman
    source: :Marie_Therese_of_Wurttemberg
  AssignClass (8ea0ac99-e943-4854-a6a6-e301f9a28419)
 Call ID: 8ea0ac99-e943-4854-a6a6-e301f9a28419
  Args:
    type: :Person
    source: :Marie_Therese_of_Wurttemberg
  AddLiteral (b6e8f401-85a3-41a8-a29c-3d0afefd80e7)
 Call ID: b6e8f401-85a3-41a8-a29c-3d0afefd80e7
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: :Marie_Therese_of_Wurttemberg
    literal_value: 1934
  AssignClass (72061a1b-7c19-48e0-b4c2-48c3651d02c1)
 Call ID: 72061a1b-7c19-48e0-b4c2-48c3651d02c1
  Args:
    source: :Micaela_Anna_Maria_Cousino
    type: :Woman
  AssignClass (dd5bca0d-62dc-4a54-a7cd-fd993de520ac)
 Call ID: dd5bca0d-62dc-4a54-a7cd-fd993de520ac
  Args:
    type: :Person
    source: :Micaela_Anna_Maria_Cousino
  AddLiteral (051171d4-98f0-459b-bc68-6b624e686e19)
 Call ID: 051171d4-98f0-459b-bc68-6b624e686e19
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: :Micaela_Anna_Maria_Cousino
    literal_value: 1938
  AddLiteral (c7d0a28e-b362-4d81-8ce8-9aa439357af7)
 Call ID: c7d0a28e-b362-4d81-8ce8-9aa439357af7
  Args:
    relation: :hasDeathYear
    literal_value: 2022
    source: :Micaela_Anna_Maria_Cousino
    literal_type: xsd:integer
  AddLiteral (fb5a6265-5f13-4925-b9fa-c585793717b1)
 Call ID: fb5a6265-5f13-4925-b9fa-c585793717b1
  Args:
    relation: :hasMarriageYear
    literal_value: 1984
    source: :Micaela_Anna_Maria_Cousino
    literal_type: xsd:integer
  AssignClass (585ce1d0-1d0c-4d6e-9614-1571fd11fda8)
 Call ID: 585ce1d0-1d0c-4d6e-9614-1571fd11fda8
  Args:
    source: :Luis_Cousino_y_Sebire
    type: :Man
  AssignClass (4c733bde-8027-4cea-870d-d08f41e5d027)
 Call ID: 4c733bde-8027-4cea-870d-d08f41e5d027
  Args:
    type: :Person
    source: :Luis_Cousino_y_Sebire
  AssignClass (9a4ab1b8-497d-4c98-ba73-7087dacb7223)
 Call ID: 9a4ab1b8-497d-4c98-ba73-7087dacb7223
  Args:
    source: :Antonia_Maria_Quinones_de_Leon
    type: :Woman
  AssignClass (348df9eb-3de8-4d42-ba6c-039db9bdf1d5)
 Call ID: 348df9eb-3de8-4d42-ba6c-039db9bdf1d5
  Args:
    source: :Antonia_Maria_Quinones_de_Leon
    type: :Person
  AddTriple (e251f8da-9119-4b23-adac-d2edc9a7b70f)
 Call ID: e251f8da-9119-4b23-adac-d2edc9a7b70f
  Args:
    source: :Micaela_Anna_Maria_Cousino
    relation: :hasFather
    target: :Luis_Cousino_y_Sebire
  AddTriple (ceedb171-c988-4496-b361-35460802676c)
 Call ID: ceedb171-c988-4496-b361-35460802676c
  Args:
    target: :Antonia_Maria_Quinones_de_Leon
    relation: :hasMother
    source: :Micaela_Anna_Maria_Cousino
  AssignClass (f2ab554b-31e7-4365-ba48-8a5234c4af12)
 Call ID: f2ab554b-31e7-4365-ba48-8a5234c4af12
  Args:
    type: :Man
    source: :Jean_Robert_Boeuf
  AssignClass (f0436547-eec7-4921-90ba-227380b424da)
 Call ID: f0436547-eec7-4921-90ba-227380b424da
  Args:
    type: :Person
    source: :Jean_Robert_Boeuf
  AssignClass (3cbde540-a1f3-4227-83d7-1a5e71f5121f)
 Call ID: 3cbde540-a1f3-4227-83d7-1a5e71f5121f
  Args:
    type: :Woman
    source: :Marie_dOrleans_1989
  AssignClass (b7d12a94-185d-4ab0-a9b2-e124455ba82c)
 Call ID: b7d12a94-185d-4ab0-a9b2-e124455ba82c
  Args:
    type: :Person
    source: :Marie_dOrleans_1989
  AddTriple (02bf7ca2-8194-488e-b9d0-a74f9d5ba28f)
 Call ID: 02bf7ca2-8194-488e-b9d0-a74f9d5ba28f
  Args:
    source: :Marie_dOrleans_1989
    relation: :isDaughterOf
    target: :Henri_dOrleans
  AddTriple (f48acf8c-c3c6-49c0-b3e6-32b494e97ac9)
 Call ID: f48acf8c-c3c6-49c0-b3e6-32b494e97ac9
  Args:
    target: :Marie_Therese_of_Wurttemberg
    source: :Marie_dOrleans_1989
    relation: :isDaughterOf
  AssignClass (973eb160-ae5b-45a8-b6a7-4d6ba72814ba)
 Call ID: 973eb160-ae5b-45a8-b6a7-4d6ba72814ba
  Args:
    source: :Prince_Gundakar_of_Liechtenstein
    type: :Man
  AssignClass (366c9493-9c81-4765-b14d-57041a3faa98)
 Call ID: 366c9493-9c81-4765-b14d-57041a3faa98
  Args:
    source: :Prince_Gundakar_of_Liechtenstein
    type: :Person
  AssignClass (cc33f753-1a0f-4a72-ab28-bf84ce905f26)
 Call ID: cc33f753-1a0f-4a72-ab28-bf84ce905f26
  Args:
    source: :Diane_dOrleans
    type: :Woman
  AssignClass (6a31de26-b91a-4d30-bba6-abc9e58a75fc)
 Call ID: 6a31de26-b91a-4d30-bba6-abc9e58a75fc
  Args:
    type: :Person
    source: :Diane_dOrleans
  AddTriple (5e23f108-c2c5-4662-bcf5-1fa820e144d9)
 Call ID: 5e23f108-c2c5-4662-bcf5-1fa820e144d9
  Args:
    relation: :isSisterOf
    source: :Diane_dOrleans
    target: :Henri_dOrleans
  AssignClass (ba26bc15-47a9-4236-a17b-37bf7e162e81)
 Call ID: ba26bc15-47a9-4236-a17b-37bf7e162e81
  Args:
    source: :Michel_dOrleans
    type: :Man
  AssignClass (a9568461-9f65-4d49-8cb1-10e169a1bad6)
 Call ID: a9568461-9f65-4d49-8cb1-10e169a1bad6
  Args:
    source: :Michel_dOrleans
    type: :Person
  AddTriple (4c07ad35-4afe-4171-aa7a-521dbd87cb3b)
 Call ID: 4c07ad35-4afe-4171-aa7a-521dbd87cb3b
  Args:
    source: :Michel_dOrleans
    relation: :isBrotherOf
    target: :Henri_dOrleans
  AssignClass (3c01c815-2173-4682-97cf-00d9427b0942)
 Call ID: 3c01c815-2173-4682-97cf-00d9427b0942
  Args:
    type: :Man
    source: :Thibaut_dOrleans
  AssignClass (c07c0368-4aaa-455b-bffc-e43cffe0f3f0)
 Call ID: c07c0368-4aaa-455b-bffc-e43cffe0f3f0
  Args:
    type: :Person
    source: :Thibaut_dOrleans
  AddTriple (2453f294-845f-41c8-bd95-be7dadc27c53)
 Call ID: 2453f294-845f-41c8-bd95-be7dadc27c53
  Args:
    target: :Henri_dOrleans
    source: :Thibaut_dOrleans
    relation: :isBrotherOf
  AssignClass (fae45425-9b2f-4e3d-9660-5e86f11c8526)
 Call ID: fae45425-9b2f-4e3d-9660-5e86f11c8526
  Args:
    type: :Man
    source: :Jacques_dOrleans
  AssignClass (e943ec5d-3498-4695-8dd7-35aaea37d907)
 Call ID: e943ec5d-3498-4695-8dd7-35aaea37d907
  Args:
    type: :Person
    source: :Jacques_dOrleans
  AddTriple (9ee7e5d2-c85a-4137-ada0-660e8b2b8e84)
 Call ID: 9ee7e5d2-c85a-4137-ada0-660e8b2b8e84
  Args:
    source: :Jacques_dOrleans
    relation: :isBrotherOf
    target: :Henri_dOrleans
  AssignClass (3fbfef4b-8081-4370-b66c-278cae4b8d95)
 Call ID: 3fbfef4b-8081-4370-b66c-278cae4b8d95
  Args:
    source: :Charles_Louis_dOrleans
    type: :Man
  AssignClass (ccb6b21d-5964-408c-9e2d-afcb282efa57)
 Call ID: ccb6b21d-5964-408c-9e2d-afcb282efa57
  Args:
    type: :Person
    source: :Charles_Louis_dOrleans
  AddLiteral (d42791d7-f3a7-4115-a7ba-5f2e9d2a03a7)
 Call ID: d42791d7-f3a7-4115-a7ba-5f2e9d2a03a7
  Args:
    source: :Charles_Louis_dOrleans
    literal_value: 1972
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddTriple (f4d64a9a-cf0b-4de1-b764-57516a50127d)
 Call ID: f4d64a9a-cf0b-4de1-b764-57516a50127d
  Args:
    target: :Jacques_dOrleans
    relation: :isSonOf
    source: :Charles_Louis_dOrleans
  AssignClass (1d3c25d0-3197-4e94-a1ea-1a4382abb8f5)
 Call ID: 1d3c25d0-3197-4e94-a1ea-1a4382abb8f5
  Args:
    source: :Foulques_dOrleans
    type: :Man
  AssignClass (4bc52eaf-0e16-4a50-8bb3-a99451f2a675)
 Call ID: 4bc52eaf-0e16-4a50-8bb3-a99451f2a675
  Args:
    type: :Person
    source: :Foulques_dOrleans
  AddLiteral (ab0996fc-8788-46ee-a221-da2473af954c)
 Call ID: ab0996fc-8788-46ee-a221-da2473af954c
  Args:
    relation: :hasBirthYear
    source: :Foulques_dOrleans
    literal_value: 1974
    literal_type: xsd:integer
  AddTriple (a8c6a7cf-09fa-4080-bed6-2ade54236c0c)
 Call ID: a8c6a7cf-09fa-4080-bed6-2ade54236c0c
  Args:
    target: :Jacques_dOrleans
    source: :Foulques_dOrleans
    relation: :isSonOf
  AssignClass (261ac450-093e-4353-9dee-be7d75572e47)
 Call ID: 261ac450-093e-4353-9dee-be7d75572e47
  Args:
    type: :Man
    source: :Francois_dOrleans_Clermont
  AssignClass (c3eed437-b4b5-41bd-9451-433b654e8026)
 Call ID: c3eed437-b4b5-41bd-9451-433b654e8026
  Args:
    type: :Person
    source: :Francois_dOrleans_Clermont
  AddTriple (8f320365-7aa5-4d70-a97d-86db0a64bddc)
 Call ID: 8f320365-7aa5-4d70-a97d-86db0a64bddc
  Args:
    target: :Henri_dOrleans
    source: :Francois_dOrleans_Clermont
    relation: :isSonOf
  AssignClass (b89d4618-e821-4d87-888a-8551f7a90fda)
 Call ID: b89d4618-e821-4d87-888a-8551f7a90fda
  Args:
    source: :Jean_dOrleans
    type: :Man
  AssignClass (b5664c4b-22ab-43ea-964a-5ad24ed5c319)
 Call ID: b5664c4b-22ab-43ea-964a-5ad24ed5c319
  Args:
    type: :Person
    source: :Jean_dOrleans
  AddTriple (86d65eff-74e6-4ca0-902a-08fa58075453)
 Call ID: 86d65eff-74e6-4ca0-902a-08fa58075453
  Args:
    source: :Jean_dOrleans
    relation: :isSonOf
    target: :Henri_dOrleans
  AssignClass (9d373711-a7e1-4cb6-afb3-648c1b1b369a)
 Call ID: 9d373711-a7e1-4cb6-afb3-648c1b1b369a
  Args:
    type: :Man
    source: :Louis_Alphonse_Duke_of_Anjou
  AssignClass (78c693f0-f2fc-435f-8740-cb9271183da6)
 Call ID: 78c693f0-f2fc-435f-8740-cb9271183da6
  Args:
    source: :Louis_Alphonse_Duke_of_Anjou
    type: :Person
  Finish (d94789fa-ea06-4aa3-94a1-4baf233b3afd)
 Call ID: d94789fa-ea06-4aa3-94a1-4baf233b3afd
  Args: